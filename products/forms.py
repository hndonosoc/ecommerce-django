from django import forms
from .models import Product, ProductImage

class ProductForm(forms.ModelForm):
    imagen_principal = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Product
        fields = ["nombre", "descripcion", "precio", "stock", "categoria", "activo"]

        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: Notebook Gamer"
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Descripción del producto..."
            }),
            "precio": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "Ej: 499.90"
            }),
            "stock": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Cantidad disponible"
            }),
            "categoria": forms.Select(attrs={
                "class": "form-select"
            }),
            "activo": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

    def clean_precio(self):
        precio = self.cleaned_data.get("precio")
        if precio is None or precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a 0.")
        return precio

    def clean_stock(self):
        stock = self.cleaned_data.get("stock")
        if stock is not None and stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo.")
        return stock