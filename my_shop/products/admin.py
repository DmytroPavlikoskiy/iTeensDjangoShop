from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, ProductImage, Feature, ProductFeatureValue

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px; border-radius: 5px;">')
        return "Немає зображення"
    image_preview.short_description = "Попередній перегляд"


class ProductFeatureValueInline(admin.TabularInline):
    model = ProductFeatureValue
    extra = 1
    autocomplete_fields = ['feature'] 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'image_show']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_filter = ['parent']

    def image_show(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: 50px; height: 50px; object-fit: cover;">')
        return "-"
    image_show.short_description = "Фото"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'image_show', 'name', 'price', 'stock', 
        'available', 'is_featured', 'category', 'updated_at'
    ]
    list_filter = ['available', 'is_featured', 'category', 'created_at']
<<<<<<< Updated upstream
    list_editable = ['price', 'stock', 'available', 'is_featured'] 
=======
    list_editable = ['price', 'stock', 'available', 'is_featured']
>>>>>>> Stashed changes
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductFeatureValueInline, ProductImageInline]
    list_per_page = 20
    save_on_top = True 

    fieldsets = (
        ("Основне", {
            "fields": ("category", "name", "slug", "price")
        }),
        ("Статус та склад", {
            "fields": ("stock", "available", "is_featured"),
        }),
        ("Опис", {
            "fields": ("short_description", "description"),
            "classes": ("collapse",) 
        }),
    )

    def image_show(self, obj):
        if obj.images.exists(): 
            img_url = obj.images.first().image.url
            return mark_safe(f'<img src="{img_url}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 4px;">')
        return "Нет фото"
    image_show.short_description = "Фото"


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit']
<<<<<<< Updated upstream
    search_fields = ['name']
=======
    search_fields = ['name']
>>>>>>> Stashed changes
