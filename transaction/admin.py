from django.contrib import admin
from .models import Transaction, Beneficiaries, BankInfo, Autopayment, Notifications, Review


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'provider', 'amount',
                    'status', 'date', 'reciever_number')
    search_fields = ('user', 'provider')
    list_filter = ('status', 'provider')
    date_hierarchy = 'date'
    search_fields = ('user', 'provider', 'reciever_number', '')
    ordering = ('-date',)


class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'provider', 'name', 'user_code')
    search_fields = ('user', 'provider', 'name')
    list_filter = ('provider',)


class BankInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'account_status', 'bank_name')
    search_fields = ('user', 'bank_name')
    list_filter = ('bank_name',)


class AutopaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'service_provider',
                    'number', 'amount_plan', 'end_date')
    search_fields = ('user', 'name', 'service_provider')
    list_filter = ('service_provider', 'period')


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'type')
    search_fields = ('user', 'type')
    list_filter = ('type',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'star')
    search_fields = ('user', 'star')
    list_filter = ('star',)


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Beneficiaries, BeneficiaryAdmin)
admin.site.register(BankInfo, BankInfoAdmin)
admin.site.register(Autopayment, AutopaymentAdmin)
admin.site.register(Notifications, NotificationAdmin)
