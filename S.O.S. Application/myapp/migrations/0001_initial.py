# Generated by Django 4.2.2 on 2023-06-26 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('CourierID', models.IntegerField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=45, null=True)),
                ('Surname', models.CharField(max_length=45, null=True)),
                ('Phone', models.CharField(max_length=45, null=True)),
                ('LicenseType', models.CharField(max_length=45, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('CurrencyType', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('ExchangeRate', models.DecimalField(decimal_places=2, max_digits=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('DistrictID', models.IntegerField(primary_key=True, serialize=False)),
                ('DistrictName', models.CharField(max_length=45, null=True)),
                ('Coordination', models.CharField(max_length=45, null=True)),
                ('Population', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('DonationID', models.IntegerField(primary_key=True, serialize=False)),
                ('DonationTime', models.DateField(null=True)),
                ('DonationDeliveryTime', models.DateField(null=True)),
                ('RequestID', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Donator',
            fields=[
                ('DonatorID', models.IntegerField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=225, null=True)),
                ('Surname', models.CharField(max_length=225, null=True)),
                ('Phone', models.CharField(max_length=45, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('ItemID', models.IntegerField(primary_key=True, serialize=False)),
                ('ItemCategory', models.CharField(max_length=45, null=True)),
                ('Amount', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LogisticsCompany',
            fields=[
                ('CompanyID', models.IntegerField(primary_key=True, serialize=False)),
                ('CompanyName', models.CharField(max_length=45, null=True)),
                ('Phone', models.CharField(max_length=45, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('PurchaseTransactionID', models.IntegerField(primary_key=True, serialize=False)),
                ('TransactionCost', models.DecimalField(decimal_places=2, max_digits=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('RequestID', models.IntegerField(primary_key=True, serialize=False)),
                ('RequestTime', models.DateField(null=True)),
                ('CurrentStatus', models.CharField(max_length=45, null=True)),
                ('DeliveryTime', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('SupplierID', models.IntegerField(primary_key=True, serialize=False)),
                ('SupplierName', models.CharField(max_length=45, null=True)),
                ('Phone', models.CharField(max_length=45, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('VehicleID', models.IntegerField(primary_key=True, serialize=False)),
                ('VehicleType', models.CharField(max_length=45, null=True)),
                ('Capacity', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Victim',
            fields=[
                ('RequesterID', models.IntegerField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=225, null=True)),
                ('Surname', models.CharField(max_length=225, null=True)),
                ('Address', models.CharField(max_length=225, null=True)),
                ('PhoneNumber', models.CharField(max_length=45, null=True)),
                ('District_DistrictID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.district')),
            ],
        ),
        migrations.CreateModel(
            name='Request_Vehicle_Courier_Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DeliveryTime', models.DateField(null=True)),
                ('Courier_CourierID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.courier')),
                ('Request_RequestID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.request')),
                ('Vehicle_VehicleID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='Request_has_LogisticsCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DeliveryTime', models.DateField(null=True)),
                ('LogisticsCompany_CompanyID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.logisticscompany')),
                ('Request_RequestID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.request')),
            ],
        ),
        migrations.CreateModel(
            name='Request_has_Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantity', models.IntegerField(null=True)),
                ('Items_ItemID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.items')),
                ('Request_RequestID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.request')),
            ],
        ),
        migrations.AddField(
            model_name='request',
            name='Victim_RequesterID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.victim'),
        ),
        migrations.CreateModel(
            name='Purchase_has_Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Purchase_PurchaseTransactionID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.purchase')),
                ('Supplier_SupplierID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase_has_Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Amount', models.IntegerField(null=True)),
                ('UnitItemCost', models.DecimalField(decimal_places=2, max_digits=2, null=True)),
                ('Items_ItemID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.items')),
                ('Purchase_PurchaseTransactionID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.purchase')),
            ],
        ),
        migrations.CreateModel(
            name='LogisticsCompany_has_District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CostOfOutsource', models.DecimalField(decimal_places=2, max_digits=2, null=True)),
                ('District_DistrictID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.district')),
                ('LogisticsCompany_CompanyID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.logisticscompany')),
            ],
        ),
        migrations.CreateModel(
            name='Donation_has_Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantity', models.IntegerField(null=True)),
                ('Donation_DonationID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.donation')),
                ('Items_ItemID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.items')),
            ],
        ),
        migrations.CreateModel(
            name='Donation_has_Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Amount', models.IntegerField(null=True)),
                ('Currency_CurrencyType', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.currency')),
                ('Donation_DonationID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.donation')),
            ],
        ),
        migrations.AddField(
            model_name='donation',
            name='Donator_DonatorID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.donator'),
        ),
        migrations.AddField(
            model_name='donation',
            name='Request_RequestID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.request'),
        ),
    ]