from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.contrib.auth import authenticate
from datetime import datetime
from .models import Cliente, Factura, DetalleFactura
from inventario.models import Producto
import inventario.views as inventario
from .forms import ClienteForm
from django.contrib import messages
from bases.views import SinPrivilegios


class crearVistaBase(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    context_object_name = 'obj'
    success_message = "Registro agregado correctamente"

    def form_valid(self, form):
        form.instance.usuarioCrea = self.request.user

        return super().form_valid(form)


class editarVistaBase(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    context_object_name = 'obj'
    success_message = "Registro actualizado correctamente"

    def form_valid(self, form):
        form.instance.usuarioModifica = self.request.user.id

        return super().form_valid(form)


class listarClientes(SinPrivilegios, generic.ListView):
    model = Cliente
    template_name = "facturacion/listaClientes.html"
    context_object_name = "clientes"
    permission_required = "facturacion.view_cliente"


class nuevoCliente(crearVistaBase):
    model = Cliente
    template_name = "facturacion/formCliente.html"
    form_class = ClienteForm
    success_url = reverse_lazy("facturacion:listaClientes")
    permission_required = "facturacion.add_cliente"


class editarCliente(editarVistaBase):
    model = Cliente
    template_name = "facturacion/formCliente.html"
    form_class = ClienteForm
    success_url = reverse_lazy("facturacion:listaClientes")
    permission_required = "facturacion.change_cliente"


@login_required(login_url="/login/")
@permission_required("facturacion.change_cliente", login_url="/login/")
def estadoCliente(request, idCliente):
    cliente = Cliente.objects.filter(pk=idCliente).first()

    if request.method == "POST":
        if cliente:
            cliente.estado = not cliente.estado

            cliente.save()

            return HttpResponse("Ok")

        return HttpResponse("Fail")

    return HttpResponse("Fail")


class listarFacturas(SinPrivilegios, generic.ListView):
    model = Factura
    template_name = "facturacion/listaFacturas.html"
    context_object_name = "facturas"
    permission_required = "facturacion.view_factura"


@login_required(login_url='/login/')
@permission_required('facturacion.change_factura', login_url='bases:sinPrivilegios')
def nuevaFactura(request, id=None):
    template_name = 'facturacion/nuevaFactura.html'
    detalleFactura = {}
    clientes = Cliente.objects.filter(estado=True)

    if request.method == "GET":
        factura = Factura.objects.filter(pk=id).first()

        if not factura:
            encabezado = {
                'id': 0,
                'fecha': datetime.today(),
                'cliente': 0,
                'subTotal': 0.00,
                'descuento': 0.00,
                'total': 0.00
            }

            detalleFactura = None
        else:
            encabezado = {
                'id': factura.id,
                'fecha': factura.fecha,
                'cliente': factura.cliente,
                'subTotal': factura.subTotal,
                'descuento': factura.descuento,
                'total': factura.total
            }

        detalleFactura = DetalleFactura.objects.filter(factura=factura)

        contexto = {
            "factura": encabezado,
            "detalleFactura": detalleFactura,
            "clientes": clientes
        }

        return render(request, template_name, contexto)

    if request.method == "POST":
        idCliente = request.POST.get("cliente")
        fecha = request.POST.get("fecha")
        cliente = Cliente.objects.get(pk=idCliente)

        if not id:
            factura = Factura(cliente=cliente, fecha=fecha)

            if factura:
                factura.save()

                id = factura.id
        else:
            factura = Factura.objects.filter(pk=id).first()

            if factura:
                factura.cliente = cliente

                factura.save()

        if not id:
            messages.error(request, 'No se puede detectar el Nr. de factura')
            
            return redirect("facturacion:listaFacturas")

        codigo = request.POST.get("codigo")
        cantidad = request.POST.get("cantidad")
        precio = request.POST.get("precio")
        subTotalDetalle = request.POST.get("subTotalDetalle")
        descuentoDetalle = request.POST.get("descuentoDetalle")
        totalDetalle = request.POST.get("totalDetalle")
        producto = Producto.objects.get(codigo=codigo)
        
        detalleFactura = DetalleFactura(factura=factura, producto=producto, cantidad=cantidad, precio=precio, subTotalDetalle=subTotalDetalle, descuentoDetalle=descuentoDetalle, totalDetalle=totalDetalle)
        
        if detalleFactura:
            detalleFactura.save()
            
        return redirect("facturacion:editarFactura", id=id)

    return render(request, template_name, contexto)


class verProductos(inventario.listarProductos):
    template_name = "facturacion/buscarProducto.html"


def borrarDetalleFactura(request, id):
    template_name = "facturacion/borrarDetalleFactura.html"
    detalleFactura = DetalleFactura.objects.get(pk=id)

    if request.method == "GET":
        contexto = {"detalleFactura": detalleFactura}

    if request.method == "POST":
        user = request.POST.get("usuario")
        password = request.POST.get("password")
        usuario = authenticate(username=user, password=password)

        if not usuario:
            return HttpResponse("Usuario o contraseña incorrecta")

        if not usuario.is_active:
            return HttpResponse("Usuario inactivo")

        if usuario.is_superuser or usuario.has_perm("facturacion.sup_caja_detalleFactura"):
            detalleFactura.id = None
            detalleFactura.cantidad = (-1 * detalleFactura.cantidad)
            detalleFactura.subTotalDetalle = (-1 * detalleFactura.subTotalDetalle)
            detalleFactura.descuentoDetalle = (-1 * detalleFactura.descuentoDetalle)
            detalleFactura.totalDetalle = (-1 * detalleFactura.totalDetalle)

            detalleFactura.save()

            return HttpResponse("Ok")

        return HttpResponse("Usuario no autorizado")

    return render(request, template_name, contexto)
