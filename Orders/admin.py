from django.contrib import admin
from .models import CoponModel,OrderModel,OrderItemsModel
# Register your models here.

admin.site.register(CoponModel)
class ProductItemLine(admin.TabularInline):
    model = OrderItemsModel

@admin.register(OrderModel)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductItemLine,)