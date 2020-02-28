import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils import timezone
from .models import Compra, DetalleCompra


def link_callback(uri, rel):
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri

    if not os.path.isfile(path):
        raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))

    return path


def reporteCompras(request):
    template_path = 'compra/imprimirCompras.html'
    today = timezone.now()
    compras = Compra.objects.all()
    contexto = {
        'compras': compras,
        'today': today,
        'request': request
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte.pdf"'
    template = get_template(template_path)
    html = template.render(contexto)
    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    if pisaStatus.err:
        return HttpResponse('Tuvimos algunos errores <pre>' + html + '</pre>')

    return response


def reporteCompra(request, idCompra):
    template_path = 'compra/imprimirCompra.html'
    today = timezone.now()
    compra = Compra.objects.filter(id=idCompra).first()

    if compra:
        # detalleCompras = DetalleCompra.objects.filter(idCompra=idCompra)
        detalleCompras = DetalleCompra.objects.filter(compra__id=idCompra)
    else:
        detalleCompras = {}

    contexto = {
        'detalleCompras': detalleCompras,
        'compra': compra,
        'today': today,
        'request': request
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte.pdf"'
    template = get_template(template_path)
    html = template.render(contexto)
    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    if pisaStatus.err:
        return HttpResponse('Tuvimos algunos errores <pre>' + html + '</pre>')

    return response
