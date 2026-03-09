from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Product
from django.contrib.auth.decorators import login_required, user_passes_test

def es_admin(user):
    return user.is_superuser


def product_list(request):
    """Lista simple de productos para el área administrativa o listado interno"""
    productos = Product.objects.select_related("categoria").order_by("-id")
    return render(request, "products/product_list.html", {"productos": productos})


@login_required
@user_passes_test(es_admin)
def admin_productos(request):
    productos = Product.objects.all().select_related("categoria")
    return render(request, 'products/admin_productos.html', {'productos': productos})

@login_required
@user_passes_test(es_admin)
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect("products:admin_productos")
    else:
        form = ProductForm()
    return render(request, "products/product_form.html", {"form": form, "accion": "Crear"})

@login_required
@user_passes_test(es_admin)
def product_edit(request, pk):
    producto = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect("products:admin_productos")
    else:
        form = ProductForm(instance=producto)
    return render(request, "products/product_form.html", {"form": form, "producto": producto, "accion": "Editar"})

@login_required
@user_passes_test(es_admin)
def product_delete(request, pk):
    producto = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        producto.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect("products:admin_productos")
    return render(request, "products/product_confirm_delete.html", {"producto": producto})