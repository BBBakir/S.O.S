from django.contrib import admin
from .models import *

admin.site.register(District)
admin.site.register(Victim)
admin.site.register(Request)
admin.site.register(Items)
admin.site.register(Donator)
admin.site.register(Donation)
admin.site.register(Currency)
admin.site.register(Purchase)
admin.site.register(LogisticsCompany)
admin.site.register(Courier)
admin.site.register(Request_has_Items)
admin.site.register(Donation_has_Items)
admin.site.register(Donation_has_Currency)
admin.site.register(Purchase_has_Items)
admin.site.register(LogisticsCompany_has_District)
admin.site.register(Vehicle)
admin.site.register(Request_Vehicle_Courier_Assignment)
admin.site.register(Request_has_LogisticsCompany)
admin.site.register(Supplier)
admin.site.register(Purchase_has_Supplier)


