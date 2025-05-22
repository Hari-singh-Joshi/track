from django.contrib import admin
from .models import ExpensePayment
#here we register admin dashboard functionalty
@admin.register(ExpensePayment)
class ExpensePaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'category', 'date', 'status', 'created_at')
    list_filter = ('category', 'status', 'date')
    search_fields = ('user__username', 'description', 'order_id', 'payment_id')
    readonly_fields = ('created_at',)
