from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    # list_display = ['id', 'user', 'totalNum', 'totalMoney', 'submitDate', 'paid', 'consign', 'consignDate']
    list_filter = ['paid', 'submitDate', 'consign', 'consignDate']
    date_hierarchy = 'submitDate'
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
