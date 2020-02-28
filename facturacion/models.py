from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from bases.models import ClaseModelo, ClaseModelo2
from inventario.models import Producto


class Cliente(ClaseModelo):
    NAT = 'Natural'
    JUR = 'Juridica'
    TIPOCLIENTE = [(NAT, 'Natural'), (JUR, 'Juridica')]
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    celular = models.CharField(max_length=20, null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPOCLIENTE, default=NAT)

    def __str__(self):
        return '{} {}'.format(self.apellidos, self.nombres)

    def save(self):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()

        super(Cliente, self).save()

    class Meta:
        verbose_name_plural = "Clientes"


class Factura(ClaseModelo2):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    subTotal = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    total = models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.id)

    def save(self):
        self.total = self.subTotal - self.descuento

        super(Factura, self).save()

    class Meta:
        verbose_name_plural = "Facturas"
        verbose_name = "Factura"
        permissions = [
            ('sup_caja_factura', 'Permisos de supervisor de caja Factura')
        ]


class DetalleFactura(ClaseModelo2):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.BigIntegerField(default=0)
    precio = models.FloatField(default=0)
    subTotalDetalle = models.FloatField(default=0)
    descuentoDetalle = models.FloatField(default=0)
    totalDetalle = models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.producto)

    def save(self):
        self.subTotalDetalle = float(float(int(self.cantidad)) * float(self.precio))
        self.totalDetalle = self.subTotalDetalle - float(self.descuentoDetalle)

        super(DetalleFactura, self).save()

    class Meta:
        verbose_name_plural = "Detalle facturas"
        verbose_name = "Detalle factura"
        permissions = [
            ('sup_caja_detalleFactura', 'Permisos de supervisor de caja Detalle Factura')
        ]


@receiver(post_save, sender=DetalleFactura)
def guardarDetalleFactura(sender, instance, **kwargs):
    idProducto = instance.producto.id
    idFactura = instance.factura.id
    factura = Factura.objects.get(pk=idFactura)

    if factura:
        subTotal = DetalleFactura.objects.filter(factura=idFactura).aggregate(subTotal=Sum('subTotalDetalle')).get('subTotal', 0.00)
        descuento = DetalleFactura.objects.filter(factura=idFactura).aggregate(descuento=Sum('descuentoDetalle')).get('descuento', 0.00)
        factura.subTotal = subTotal
        factura.descuento = descuento

        factura.save()

    producto = Producto.objects.filter(pk=idProducto).first()

    if producto:
        cantidad = int(producto.existencia) - int(instance.cantidad)
        producto.existencia = cantidad

        producto.save()
