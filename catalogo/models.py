from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pedidos")
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    completado = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario.username}"

class OrderItem(models.Model):
    pedido = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto.nombre if self.producto else 'Producto eliminado'} x {self.cantidad}"

    @property
    def subtotal(self):
        """Calcula el subtotal directamente en el modelo"""
        return self.precio * self.cantidad