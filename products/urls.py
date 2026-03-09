from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("admin/", views.admin_productos, name="admin_productos"),
    path("create/", views.product_create, name="create"),
    path("edit/<int:pk>/", views.product_edit, name="edit"),
    path("delete/<int:pk>/", views.product_delete, name="delete"),
]