from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
import datetime
import json
from django.db.models import Sum
from .models import Proveedor, Compra, DetalleCompra
from .forms import ProveedorForm, CompraForm
from django.urls import reverse_lazy
from bases.views import SinPrivilegios
from inventario.models import Producto


class listarProveedores(SinPrivilegios, generic.ListView):
    model = Proveedor
    template_name = "compra/listaProveedores.html"
    context_object_name = "proveedores"
    permission_required = "compra.view_proveedor"


class listarCompras(SinPrivilegios, generic.ListView):
    model = Compra
    template_name = "compra/listaCompras.html"
    context_object_name = "compras"
    permission_required = "compra.view_compra"


class nuevoProveedor(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    model = Proveedor
    template_name = "compra/formProveedor.html"
    context_object_name = "proveedor"
    permission_required = "compra.add_proveedor"
    form_class = ProveedorForm
    success_url = reverse_lazy("compra:listaProveedores")

    def form_valid(self, form):
        form.instance.usuarioCrea = self.request.user

        return super().form_valid(form)


@login_required(login_url='/login/')
@permission_required('compra.view_compra', login_url='bases:sinPrivilegios')
def nuevaCompra(request, idCompra=None):
    template_name = "compra/formCompra.html"
    productos = Producto.objects.filter(estado=True)
    formCompra = {}
    contexto = {}

    if request.method == 'GET':
        formCompra = CompraForm()
        compra = Compra.objects.filter(pk=idCompra).first()

        if compra:
            detalleCompra = DetalleCompra.objects.filter(compra=compra)
            fechaCompra = datetime.date.isoformat(compra.fechaCompra)
            fechaFactura = datetime.date.isoformat(compra.fechaFactura)
            datos = {
                'fechaCompra': fechaCompra,
                'proveedor': compra.proveedor,
                'observacion': compra.observacion,
                'numFactura': compra.numFactura,
                'fechaFactura': fechaFactura,
                'subTotal': compra.subTotal,
                'descuento': compra.descuento,
                'total': compra.total
            }
            formCompra = CompraForm(datos)
        else:
            detalleCompra = None

        contexto = {'productos': productos, 'compra': compra, 'detalles': detalleCompra, 'formCompra': formCompra}

        # return render(request, template_name, contexto)

    if request.method == 'POST':
        # Compra
        fechaCompra = request.POST.get("fechaCompra")
        observacion = request.POST.get("observacion")
        numFactura = request.POST.get("numFactura")
        fechaFactura = request.POST.get("fechaFactura")
        proveedor = request.POST.get("proveedor")
        subTotal = 0
        descuento = 0
        total = 0

        if not idCompra:
            proveedor = Proveedor.objects.get(pk=proveedor)
            compra = Compra(fechaCompra=fechaCompra, observacion=observacion, numFactura=numFactura, fechaFactura=fechaFactura, proveedor=proveedor, usuarioCrea=request.user)

            if compra:
                compra.save()
                idCompra = compra.id
        else:
            compra = Compra.objects.filter(pk=idCompra).first()

            if compra:
                compra.fechaCompra = fechaCompra
                compra.observacion = observacion
                compra.numFactura = numFactura
                compra.fechaFactura = fechaFactura
                compra.usuarioModifica = request.user.id
                compra.save()

        if not idCompra:
            return redirect("compra:listaCompras")

        # DetalleCompra
        producto = request.POST.get("id_idProducto")
        cantidad = request.POST.get("id_cantidadDetalle")
        precio = request.POST.get("id_precioDetalle")
        subtotal = request.POST.get("id_subtotalDetalle")
        descuento = request.POST.get("id_descuentoDetalle")
        total = request.POST.get("id_totalDetalle")
        producto = Producto.objects.get(pk=producto)

        detalleCompra = DetalleCompra(compra=compra, producto=producto, cantidad=cantidad, precio=precio, descuento=descuento, costo=0, usuarioCrea=request.user)

        if detalleCompra:
            detalleCompra.save()

            subTotal = DetalleCompra.objects.filter(compra=idCompra).aggregate(Sum('subTotal'))
            descuento = DetalleCompra.objects.filter(compra=idCompra).aggregate(Sum('descuento'))
            compra.subTotal = subTotal["subTotal__sum"]
            compra.descuento = descuento["descuento__sum"]

            compra.save()

        return redirect("compra:editarCompra", idCompra=idCompra)

    return render(request, template_name, contexto)

class editarProveedor(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    model = Proveedor
    template_name = "compra/formProveedor.html"
    context_object_name = "proveedor"
    permission_required = "compra.change_proveedor"
    form_class = ProveedorForm
    success_url = reverse_lazy("compra:listaProveedores")

    def form_valid(self, form):
        form.instance.usuarioModifica = self.request.user.id

        return super().form_valid(form)


@login_required(login_url='/login/')
@permission_required('compra.change_proveedor', login_url='bases:sinPrivilegios')
def inactivarProveedor(request, id):
    template_name = 'compra/inactivarProveedor.html'
    contexto = {}
    proveedor = Proveedor.objects.filter(pk=id).first()

    if not proveedor:
        return HttpResponse('Proveedor no existe ' + str(id))

    if request.method == 'GET':
        contexto = {'obj': proveedor}

    if request.method == 'POST':
        proveedor.estado = False

        proveedor.save()

        contexto = {'obj': 'OK'}

        return HttpResponse('Proveedor inactivado')

    return render(request, template_name, contexto)


class eliminarDetalleCompra(SinPrivilegios, generic.DeleteView):
    permission_required = "compra.delete_detallecompra"
    model = DetalleCompra
    template_name = "compra/eliminarDetalleCompra.html"
    context_object_name = "obj"

    def get_success_url(self):
        idCompra = self.kwargs['idCompra']

        return reverse_lazy('compra:editarCompra', kwargs={'idCompra': idCompra})
