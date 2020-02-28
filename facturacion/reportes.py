from django.shortcuts import render

from .models import Factura, DetalleFactura


def imprimirFactura(request, id):
    template_name = "facturacion/imprimirFactura.html"
    factura = Factura.objects.get(id=id)
    detalleFactura = DetalleFactura.objects.filter(factura=id)

    contexto = {
        'request': request,
        'factura': factura,
        'detalleFactura': detalleFactura
    }

    return render(request, template_name, contexto)