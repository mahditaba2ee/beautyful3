from django.contrib import admin
from .models import CategoryModel,TypeProductModel,BrandModel,ProductModel,ImageProductModel,ImagdeSlidModel
# Register your models here.
admin.site.register(CategoryModel)
admin.site.register(TypeProductModel)
admin.site.register(BrandModel)
admin.site.register(ImagdeSlidModel)



class ImageItemLine(admin.TabularInline):
    model = ImageProductModel

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ImageItemLine,)