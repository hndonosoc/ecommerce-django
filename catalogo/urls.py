from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path("producto/<int:pk>/", views.producto_detalle, name="producto_detalle"),
    path("contacto/", views.contacto, name="contacto"),
    path("carrito/", views.ver_carrito, name="ver_carrito"),
    path("carrito/agregar/<int:producto_id>/", views.agregar_al_carrito, name="agregar_al_carrito"),
    path("carrito/quitar/<int:producto_id>/", views.quitar_del_carrito, name="quitar_del_carrito"),
    path("registro/", views.registro, name="registro"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("checkout/", views.checkout, name="checkout"),
    path('admin/productos/', views.lista_productos_admin, name='listar_productos'),
    path('producto/nuevo/', views.gestionar_producto, name='crear_producto'),
    path('producto/editar/<int:id>/', views.gestionar_producto, name='editar_producto'),
    path('producto/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
]