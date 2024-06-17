from django.contrib import admin
from .models import Transaction, Beneficiaries, BankInfo

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user','provider', 'amount', 'status', 'date', 'reciever_number')

class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'name',)

class BankInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'account_status', 'bank_name')

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Beneficiaries, BeneficiaryAdmin)
admin.site.register(BankInfo, BankInfoAdmin)