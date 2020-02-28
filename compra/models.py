from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from bases.models import ClaseModelo
from inventario.models import Producto


class Proveedor(ClaseModelo):
    descripcion = models.CharField(max_length=100, unique=True)
    direccion = models.CharField(max_length=250, null=True, blank=True)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    correo = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.descripcion)

    def guardar(self):
        self.descripcion = self.descripcion.upper()
        super(Proveedor, self).save()

    class Meta:
        verbose_name_plural = "Proveedores"


class Compra(ClaseModelo):
    fechaCompra = models.DateField(null=True, blank=True)
    observacion = models.TextField(blank=True, null=True)
    numFactura = models.CharField(max_length=100)
    fechaFactura = models.DateField()
    subTotal = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    
    def __str__(self):
        return '{}'.format(self.observacion)

    def save(self):
        self.observacion = self.observacion.upper()
        self.total = self.subTotal - self.descuento

        super(Compra, self).save()

    class Meta:
        verbose_name_plural = "Compras"
        verbose_name = "Compra"


class DetalleCompra(ClaseModelo):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.BigIntegerField(default=0)
    precio = models.FloatField(default=0)
    subTotal = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)
    costo = models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.producto)

    def save(self):
        self.subTotal = float(float(int(self.cantidad)) * float(self.precio))
        self.total = self.subTotal - float(self.descuento)

        super(DetalleCompra, self).save()

    class Meta:
        verbose_name_plural = "Detalle compras"
        verbose_name = "Detalle compra"


@receiver(post_delete, sender=DetalleCompra)
def eliminarDetalleCompra(sender, instance, **kwargs):
    idProducto = instance.producto.id
    idCompra = instance.compra.id
    compra = Compra.objects.filter(pk=idCompra).first()

    if compra:
        subTotal = DetalleCompra.objects.filter(compra=idCompra).aggregate(Sum('subTotal'))
        descuento = DetalleCompra.objects.filter(compra=idCompra).aggregate(Sum('descuento'))
        compra.subTotal = subTotal['subTotal__sum']
        compra.descuento = descuento['descuento__sum']

        compra.save()

    producto = Producto.objects.filter(pk=idProducto).first()

    if producto:
        cantidad = int(producto.existencia) - int(instance.cantidad)
        producto.existencia = cantidad

        producto.save()


@receiver(post_save, sender=DetalleCompra)
def guardarDetalleCompra(sender, instance, **kwargs):
    idProducto = instance.producto.id
    fechaCompra = instance.compra.fechaCompra
    producto = Producto.objects.filter(pk=idProducto).first()

    if producto:
        cantidad = int(producto.existencia) + int(instance.cantidad)
        producto.existencia = cantidad
        producto.ultimaCompra = fechaCompra

        producto.save()
