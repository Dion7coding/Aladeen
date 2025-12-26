from django.contrib import admin
from .models import Snack, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price',)

@admin.register(Snack)
class SnackAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available', 'stock')
    list_filter = ('is_available',)
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'lab_name', 'system_number', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('lab_name', 'system_number')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at',)

