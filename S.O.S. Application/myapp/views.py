from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from io import StringIO

import csv
from django.http import HttpResponse

from django.contrib import messages
from .forms import *
from django.contrib.auth import update_session_auth_hash
from .models import *

from .models import Victim, Items, District

from django.db.models import Max


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            user_id = Victim.objects.aggregate(Max('RequesterID'))
            if user_id['RequesterID__max'] is not None:
                user_id = user_id['RequesterID__max'] + 1
            else:
                user_id = 1
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login(request):
    form = UserCreationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = UserUpdateForm(request.POST, instance=request.user)

        if profile_form.is_valid():
            user = profile_form.save()

            # If a new password is provided, use set_password to hash it before saving
            if profile_form.cleaned_data.get('password1'):
                user.set_password(profile_form.cleaned_data.get('password1'))
                user.save()

                # Update the user's session to prevent logout
                update_session_auth_hash(request, user)

            messages.success(request, 'Your profile was successfully updated!')
            return redirect('sos-home')  # Redirect to 'sos-home' page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        profile_form = UserUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {'profile_form': profile_form})


from django.db.models import Max
from .forms import DonationForm, DonatorForm
from .models import Donation, Donator

def donation_list_view(request):
    donations = Donation.objects.all()
    donators = Donator.objects.all() # To retrieve all Donators

    if request.method == 'POST':
        donation_form = DonationForm(request.POST, prefix='donation')
        donator_form = DonatorForm(request.POST, prefix='donator')
        if donation_form.is_valid():
            donation_form.save()
            return redirect('donations')
        if donator_form.is_valid():
            donator_form.save()
            return redirect('donations')
    else:
        donation_form = DonationForm(prefix='donation')
        donator_form = DonatorForm(prefix='donator')

    max_donation_id = Donation.objects.aggregate(Max('DonationID'))['DonationID__max']
    new_donation_id  = max_donation_id + 1 if max_donation_id else 1

    donation_form.fields['DonationID'].initial = new_donation_id

    context = {
        'donations': donations,
        'donation_form': donation_form,
        'donator_form': donator_form,
        'donators': donators,
    }
    return render(request, 'donations_list.html', context)

def donation_create_view(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('donations')
    else:
        form = DonationForm()
    return render(request, 'donation_create.html', {'form': form})


def donation_edit_view(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    donation_items = Donation_has_Items.objects.filter(Donation_DonationID=donation)
    donation_currencies = Donation_has_Currency.objects.filter(Donation_DonationID=donation)

    if request.method == 'POST':
        form = DonationForm(request.POST, instance=donation)

        item_forms = [DonationItemFormset(request.POST, prefix=f'item-{i}', instance=item) for i, item in
                      enumerate(donation_items)]
        currency_forms = [DonationCurrencyFormset(request.POST, prefix=f'currency-{i}', instance=currency) for
                          i, currency in enumerate(donation_currencies)]

        if form.is_valid():
            donation = form.save()

        for item_form in item_forms:
            if item_form.is_valid():
                item = item_form.save(commit=False)
                item.Donation_DonationID = donation
                item.save()

        for currency_form in currency_forms:
            if currency_form.is_valid():
                currency = currency_form.save(commit=False)
                currency.Donation_DonationID = donation
                currency.save()

        return redirect('donations')
    else:
        form = DonationForm(instance=donation)
        item_forms = [DonationItemFormset(prefix=f'item-{i}', instance=item) for i, item in enumerate(donation_items)]
        currency_forms = [DonationCurrencyFormset(prefix=f'currency-{i}', instance=currency) for i, currency in
                          enumerate(donation_currencies)]

    context = {
        'form': form,
        'item_forms': item_forms,
        'currency_forms': currency_forms
    }

    return render(request, 'donation_edit.html', context)



def donation_delete_view(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    if request.method == 'POST':
        donation.delete()
        return redirect('donations')
    return render(request, 'donation_confirm_delete.html', {'donation': donation})



def logistics_list_view(request):
    logistics_companies = LogisticsCompany.objects.all()
    logistics_districts = LogisticsCompany_has_District.objects.select_related('District_DistrictID', 'LogisticsCompany_CompanyID')

    if request.method == 'POST':
        form = AddLogisticsCompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('logistics')
    else:
        form = AddLogisticsCompanyForm()

    max_company_id = LogisticsCompany.objects.aggregate(Max('CompanyID'))['CompanyID__max']
    new_company_id = max_company_id + 1 if max_company_id else 1

    form.fields['CompanyID'].initial = new_company_id

    context = {'logistics': logistics_companies, 'logistics_districts': logistics_districts, 'form': form}
    return render(request, 'logistics_list.html', context)

def logistics_delete(request, pk):
    logistic_company = get_object_or_404(LogisticsCompany, pk=pk)
    if request.method == 'POST':
        logistic_company.delete()
        return redirect('logistics')
    return render(request, 'delete_confirm.html', {'object': logistic_company})
def logistics_update_view(request, pk):
    logistics = get_object_or_404(LogisticsCompany, pk=pk)
    districts = District.objects.all()
    logistics_districts = LogisticsCompany_has_District.objects.filter(LogisticsCompany_CompanyID=pk)
    company_requests = Request_has_LogisticsCompany.objects.filter(LogisticsCompany_CompanyID=pk)

    if request.method == 'POST':
        district_form = LogisticsCompanyHasDistrictForm(request.POST)
        if district_form.is_valid():
            new_district = district_form.save(commit=False)
            new_district.LogisticsCompany_CompanyID = logistics
            new_district.save()
            return redirect('logistics_edit', pk=pk)
    else:
        district_form = LogisticsCompanyHasDistrictForm()

    return render(request, 'logistics_update.html', {
        'logistics': logistics,
        'district_form': district_form,
        'districts': districts,
        'logistics_districts': logistics_districts,
        'company_requests': company_requests
    })


def logistics_edit_company_view(request, pk):
    logistics = get_object_or_404(LogisticsCompany, pk=pk)
    if request.method == 'POST':
        form = LogisticsCompanyForm(request.POST, instance=logistics)
        if form.is_valid():
            form.save()
            return redirect('logistics_edit', pk=pk)
    else:
        form = LogisticsCompanyForm(instance=logistics)

    return render(request, 'logistics_edit_company.html', {'form': form})

def delete_district(request, pk):
    district = get_object_or_404(LogisticsCompany_has_District, pk=pk)
    company_id = district.LogisticsCompany_CompanyID.pk
    district.delete()
    return redirect('logistics_edit', pk=company_id)

def delete_request(request, pk):
    company_request = get_object_or_404(Request_has_LogisticsCompany, pk=pk)
    company_id = company_request.LogisticsCompany_CompanyID.pk
    company_request.delete()
    return redirect('logistics_edit', pk=company_id)



from django.db.models import Sum

def expense_report(request):
    purchases = Purchase.objects.all()
    items = Items.objects.all()


    total_purchase_cost = sum(purchase.TransactionCost for purchase in purchases)

    total_logistics_cost = LogisticsCompany_has_District.objects.aggregate(Sum('CostOfOutsource'))['CostOfOutsource__sum'] or 0


    district_logistics_costs = LogisticsCompany_has_District.objects.values(
        'District_DistrictID__DistrictName').annotate(total_cost=Sum('CostOfOutsource')).order_by('-total_cost')


    district_logistics_costs = {entry['District_DistrictID__DistrictName']: entry['total_cost'] for entry in
                                district_logistics_costs}


    item_category_costs = {}
    for item in items:

        item_purchases = Purchase_has_Items.objects.filter(Items_ItemID=item.ItemID)


        item_total_cost = sum(item_purchase.UnitItemCost * item_purchase.Amount for item_purchase in item_purchases)

        if item.ItemCategory not in item_category_costs:
            item_category_costs[item.ItemCategory] = []

        item_category_costs[item.ItemCategory].append({
            'item_id': item.ItemID,
            'total_cost': item_total_cost,
        })

    for category, item_costs in item_category_costs.items():
        item_category_costs[category] = sorted(item_costs, key=lambda x: x['total_cost'], reverse=True)[:10]


    system_cost = total_purchase_cost + total_logistics_cost

    item_percentage = format((total_purchase_cost / system_cost) * 100, '.2f') if system_cost else 0
    logistics_percentage = format((total_logistics_cost / system_cost) * 100, '.2f') if system_cost else 0

    context = {
        'item_percentage': item_percentage,
        'logistics_percentage': logistics_percentage,
        'item_category_costs': item_category_costs,
        'district_logistics_costs': district_logistics_costs,
    }

    return render(request, 'report.html', context)

def export_percentages(request):
    purchases = Purchase.objects.all()
    total_purchase_cost = sum(purchase.TransactionCost for purchase in purchases)
    total_logistics_cost = LogisticsCompany_has_District.objects.aggregate(Sum('CostOfOutsource'))['CostOfOutsource__sum'] or 0
    system_cost = total_purchase_cost + total_logistics_cost
    item_percentage = format((total_purchase_cost / system_cost) * 100, '.2f') if system_cost else 0
    logistics_percentage = format((total_logistics_cost / system_cost) * 100, '.2f') if system_cost else 0

    csv_data = StringIO()
    writer = csv.writer(csv_data)
    writer.writerow(['Procurement Expenses', 'Logistics Expenses'])
    writer.writerow([item_percentage, logistics_percentage])

    response = HttpResponse(csv_data.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=percentages.csv'
    return response


def export_item_costs(request):
    items = Items.objects.all()
    item_category_costs = {}
    for item in items:
        item_purchases = Purchase_has_Items.objects.filter(Items_ItemID=item.ItemID)
        item_total_cost = sum(item_purchase.UnitItemCost * item_purchase.Amount for item_purchase in item_purchases)
        if item.ItemCategory not in item_category_costs:
            item_category_costs[item.ItemCategory] = []
        item_category_costs[item.ItemCategory].append({
            'item_id': item.ItemID,
            'total_cost': item_total_cost,
        })

    for category, item_costs in item_category_costs.items():
        item_category_costs[category] = sorted(item_costs, key=lambda x: x['total_cost'], reverse=True)[:10]

    csv_data = StringIO()
    writer = csv.writer(csv_data)
    writer.writerow(['Category', 'Item ID', 'Total Cost'])
    for category, item_costs in item_category_costs.items():
        for item in item_costs:
            writer.writerow([category, item['item_id'], item['total_cost']])

    response = HttpResponse(csv_data.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=item_costs.csv'
    return response


def export_district_costs(request):
    district_logistics_costs = LogisticsCompany_has_District.objects.values(
        'District_DistrictID__DistrictName').annotate(total_cost=Sum('CostOfOutsource')).order_by('-total_cost')

    district_logistics_costs = {entry['District_DistrictID__DistrictName']: entry['total_cost'] for entry in
                                district_logistics_costs}

    csv_data = StringIO()
    writer = csv.writer(csv_data)
    writer.writerow(['District', 'Total Logistic Cost'])
    for district, logistics_cost in district_logistics_costs.items():
        writer.writerow([district, logistics_cost])

    response = HttpResponse(csv_data.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=district_costs.csv'
    return response