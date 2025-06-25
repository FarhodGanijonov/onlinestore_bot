from django.contrib import admin
from .models import Category, Product, ColorVariant, ColorImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_ru', 'parent')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_ru')
    filter_horizontal = ('categories',)


@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'name', 'price')


@admin.register(ColorImage)
class ColorImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'color', 'image')
