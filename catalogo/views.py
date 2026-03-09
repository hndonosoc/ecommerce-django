from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, Category
from .models import Order, OrderItem, Product
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import ProductForm

def home(request):
    productos = Product.objects.filter(activo=True).order_by('-id')[:6]
    return render(request, "catalogo/home.html", {
        "productos": productos
    })

def catalogo(request):
    categoria_id = request.GET.get("categoria")
    buscar = request.GET.get("buscar")

    productos = Product.objects.filter(activo=True)

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    if buscar:
        productos = productos.filter(nombre__icontains=buscar)

    categorias = Category.objects.all()

    return render(request, "catalogo/catalogo.html", {
        "productos": productos,
        "categorias": categorias
    })

def producto_detalle(request, pk):
    producto = get_object_or_404(Product, pk=pk)
    return render(request, "catalogo/producto_detalle.html", {
        "producto": producto
    })

def contacto(request):
    if request.method == "POST":
        messages.success(request, "Tu mensaje fue enviado correctamente.")
        return redirect("home")
    return render(request, "catalogo/contacto.html")

def ver_carrito(request):
    """Vista única para visualizar el contenido del carrito."""
    carrito_session = request.session.get("carrito", {})
    items = []
    total = 0

    ids_en_carrito = [int(pid) for pid in carrito_session.keys()]
    productos_db = Product.objects.filter(id__in=ids_en_carrito)

    for producto in productos_db:
        cantidad = carrito_session.get(str(producto.id), 0)
        subtotal = producto.precio * cantidad
        total += subtotal

        items.append({
            "producto": producto,
            "cantidad": cantidad,
            "subtotal": subtotal
        })

    return render(request, "catalogo/carrito.html", {
        "items": items,
        "total": total
    })

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Product, id=producto_id)
    carrito = request.session.get("carrito", {})
    
    str_id = str(producto_id)
    cantidad_actual = carrito.get(str_id, 0)

    if cantidad_actual + 1 > producto.stock:
        messages.error(request, f"Lo sentimos, solo quedan {producto.stock} unidades de {producto.nombre}.")
    else:
        carrito[str_id] = cantidad_actual + 1
        request.session["carrito"] = carrito
        request.session.modified = True
        messages.success(request, f"{producto.nombre} agregado al carrito.")

    return redirect("ver_carrito")

def quitar_del_carrito(request, producto_id):
    carrito = request.session.get("carrito", {})
    str_id = str(producto_id)

    if str_id in carrito:
        del carrito[str_id]
        request.session["carrito"] = carrito
        request.session.modified = True
        messages.info(request, "Producto eliminado del carrito.")

    return redirect("ver_carrito")

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

@login_required
def checkout(request):
    carrito_session = request.session.get("carrito", {})
    if not carrito_session:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect("catalogo")

    items_para_pedido = []
    total = 0

    for producto_id, cantidad in carrito_session.items():
        producto = get_object_or_404(Product, id=producto_id)
        subtotal = producto.precio * cantidad
        total += subtotal
        
        items_para_pedido.append({
            "producto": producto,
            "cantidad": cantidad,
            "precio": producto.precio,
            "subtotal": subtotal
        })

    if request.method == "POST":
        for item in items_para_pedido:
            if item["producto"].stock < item["cantidad"]:
                messages.error(request, f"Lo sentimos, no hay stock suficiente de {item['producto'].nombre}.")
                return redirect("ver_carrito")

        pedido = Order.objects.create(usuario=request.user, total=total)

        for item in items_para_pedido:
            OrderItem.objects.create(
                pedido=pedido,
                producto=item["producto"],
                cantidad=item["cantidad"],
                precio=item["precio"]
            )
            
            item["producto"].stock -= item["cantidad"]
            item["producto"].save()

        request.session["carrito"] = {}
        request.session.modified = True
        
        messages.success(request, "¡Gracias por tu compra!")
        return redirect("home")

    return render(request, "catalogo/checkout.html", {
        "productos": items_para_pedido,
        "total": total
    })

def gestionar_producto(request, id=None):
    producto = get_object_or_404(Product, id=id) if id else None
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductForm(instance=producto)
        
    return render(request, 'catalogo/formulario_producto.html', {'form': form})

def lista_productos_admin(request):
    productos = Product.objects.all()
    return render(request, 'catalogo/admin_lista.html', {'productos': productos})

def eliminar_producto(request, id):
    producto = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')
    return render(request, 'catalogo/confirmar_eliminar.html', {'producto': producto})

from django.contrib.auth.decorators import user_passes_test

def es_admin(user):
    return user.is_staff

@user_passes_test(es_admin)
def lista_productos_admin(request):
    productos = Product.objects.all()
    return render(request, 'catalogo/admin_lista.html', {'productos': productos})
