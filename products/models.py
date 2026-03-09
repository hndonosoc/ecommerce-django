from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    nombre = models.CharField(max_length=120, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.nombre

class Product(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    stock = models.PositiveIntegerField(default=0)

    categoria = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="productos",
        null=True,
        blank=True
    )

    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} (${self.precio})"

    @property
    def imagen_principal(self):
        """Devuelve la primera imagen o una por defecto si no hay."""
        img = self.imagenes.order_by('orden').first()
        if img:
            return img.imagen.url
        return "/static/images/no-image.png"

class ProductImage(models.Model):
    producto = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='imagenes'
    )
    imagen = models.ImageField(upload_to='products/')
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.producto.nombre} - imagen {self.id}"
    