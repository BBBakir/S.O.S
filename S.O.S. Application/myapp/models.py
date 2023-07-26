from django.db import models


class District(models.Model):
    DistrictID = models.IntegerField(primary_key=True)
    DistrictName = models.CharField(max_length=45, null=True)
    Coordination = models.CharField(max_length=45, null=True)
    Population = models.IntegerField(null=True)

    def __str__(self):
        return self.DistrictName


class Victim(models.Model):
    RequesterID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=225, null=True)
    Surname = models.CharField(max_length=225, null=True)
    Address = models.CharField(max_length=225, null=True)
    PhoneNumber = models.CharField(max_length=45, null=True)
    District_DistrictID = models.ForeignKey(District, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.Name} {self.Surname}"


class Request(models.Model):
    RequestID = models.IntegerField(primary_key=True)
    RequestTime = models.DateField(null=True)
    CurrentStatus = models.CharField(max_length=45, null=True)
    DeliveryTime = models.DateField(null=True)
    Victim_RequesterID = models.ForeignKey(Victim, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.RequestID)


class Items(models.Model):
    ItemID = models.IntegerField(primary_key=True)
    ItemCategory = models.CharField(max_length=45, null=True)
    Amount = models.IntegerField(null=True)

    def __str__(self):
        return f"ItemID: {self.ItemID}  || {self.ItemCategory} "


class Donator(models.Model):
    DonatorID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=225, null=True)
    Surname = models.CharField(max_length=225, null=True)
    Phone = models.CharField(max_length=45, null=True)

    def __str__(self):
        return f"{self.Name} {self.Surname}"

class Donation(models.Model):
    DonationID = models.IntegerField(primary_key=True)
    DonationTime = models.DateField(null=True)
    DonationDeliveryTime = models.DateField(null=True)
    Donator_DonatorID = models.ForeignKey(Donator, on_delete=models.CASCADE, null=True)
    Request_RequestID = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.DonationID)


class Currency(models.Model):
    CurrencyType = models.CharField(max_length=45, primary_key=True)
    ExchangeRate = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.CurrencyType


class Purchase(models.Model):
    PurchaseTransactionID = models.IntegerField(primary_key=True)
    TransactionCost = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return str(self.PurchaseTransactionID)


class LogisticsCompany(models.Model):
    CompanyID = models.IntegerField(primary_key=True)
    CompanyName = models.CharField(max_length=45, null=True)
    Phone = models.CharField(max_length=45, null=True)

    def __str__(self):
        return self.CompanyName


class Courier(models.Model):
    CourierID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=45, null=True)
    Surname = models.CharField(max_length=45, null=True)
    Phone = models.CharField(max_length=45, null=True)
    LicenseType = models.CharField(max_length=45, null=True)

    def __str__(self):
        return f"{self.Name} {self.Surname}"


class Request_has_Items(models.Model):
    Request_RequestID = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)
    Items_ItemID = models.ForeignKey(Items, on_delete=models.CASCADE, null=True)
    Quantity = models.IntegerField(null=True)

    def __str__(self):
        return f"Request {self.Request_RequestID} - Items {self.Items_ItemID}"


class Donation_has_Items(models.Model):
    Donation_DonationID = models.ForeignKey(Donation, on_delete=models.CASCADE, null=True)
    Items_ItemID = models.ForeignKey(Items, on_delete=models.CASCADE, null=True)
    Quantity = models.IntegerField(null=True)

    def __str__(self):
        return f"Donation {self.Donation_DonationID} - Items {self.Items_ItemID}"


class Donation_has_Currency(models.Model):
    Donation_DonationID = models.ForeignKey(Donation, on_delete=models.CASCADE, null=True)
    Currency_CurrencyType = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
    Amount = models.IntegerField(null=True)

    def __str__(self):
        return f"Donation {self.Donation_DonationID} - Currency {self.Currency_CurrencyType}"


class Purchase_has_Items(models.Model):
    Purchase_PurchaseTransactionID = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=True)
    Items_ItemID = models.ForeignKey(Items, on_delete=models.CASCADE, null=True)
    Amount = models.IntegerField(null=True)
    UnitItemCost = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"Purchase {self.Purchase_PurchaseTransactionID} - Items {self.Items_ItemID}"


class LogisticsCompany_has_District(models.Model):
    LogisticsCompany_CompanyID = models.ForeignKey(LogisticsCompany, on_delete=models.CASCADE)
    District_DistrictID = models.ForeignKey(District, on_delete=models.CASCADE)
    CostOfOutsource = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"LogisticsCompany {self.LogisticsCompany_CompanyID} - District {self.District_DistrictID}"


class Vehicle(models.Model):
    VehicleID = models.IntegerField(primary_key=True)
    VehicleType = models.CharField(max_length=45, null=True)
    Capacity = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.VehicleType} (ID: {self.VehicleID})"


class Request_Vehicle_Courier_Assignment(models.Model):
    Request_RequestID = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)
    Courier_CourierID = models.ForeignKey(Courier, on_delete=models.CASCADE, null=True)
    Vehicle_VehicleID = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
    DeliveryTime = models.DateField(null=True)

    def __str__(self):
        return f"Assignment for Request {self.Request_RequestID}"


class Request_has_LogisticsCompany(models.Model):
    Request_RequestID = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)
    LogisticsCompany_CompanyID = models.ForeignKey(LogisticsCompany, on_delete=models.CASCADE, null=True)
    DeliveryTime = models.DateField(null=True)

    def __str__(self):
        return f"Logistics Company Assignment for Request {self.Request_RequestID}"


class Supplier(models.Model):
    SupplierID = models.IntegerField(primary_key=True)
    SupplierName = models.CharField(max_length=45, null=True)
    Phone = models.CharField(max_length=45, null=True)

    def __str__(self):
        return self.SupplierName


class Purchase_has_Supplier(models.Model):
    Purchase_PurchaseTransactionID = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=True)
    Supplier_SupplierID = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Supplier {self.Supplier_SupplierID} for Purchase {self.Purchase_PurchaseTransactionID}"



