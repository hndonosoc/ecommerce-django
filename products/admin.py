from django.contrib import admin
from .models import Product, Category, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("nombre",)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "precio",
        "stock",
        "categoria",
        "activo",
        "creado_en",
        "actualizado_en",
    )
    list_filter = ("activo", "categoria")
    search_fields = ("nombre",)
    list_editable = ("precio", "stock", "activo")
    ordering = ("-creado_en",)
    readonly_fields = ("creado_en", "actualizado_en")
    inlines = [ProductImageInline]