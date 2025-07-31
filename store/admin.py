from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # Отображаем имя и slug в списке
    prepopulated_fields = {'slug': ('name',)}  # Автоматически создаём slug из имени


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'created_at', 'image_preview')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 60px;" />'
        return "-"
    image_preview.short_description = "Превью"
    image_preview.allow_tags = True  # Позволяет отображать HTML в админке