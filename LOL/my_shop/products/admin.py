from django.contrib import admin
from .models import Category, Product, PoductImage

class PoductImageInline(admin.TabularInline):
    model = PoductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PoductImageInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)} 

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
