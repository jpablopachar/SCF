from django.urls import path, include
from .views import listarClientes, listarFacturas, verProductos, nuevoCliente, nuevaFactura, editarCliente, estadoCliente, borrarDetalleFactura
from .reportes import imprimirFactura

urlpatterns = [
    path('clientes/', listarClientes.as_view(), name="listaClientes"),
    path('facturas/', listarFacturas.as_view(), name="listaFacturas"),
    path('facturas/buscarProducto', verProductos.as_view(), name="productosFactura"),
    path('clientes/nuevoCliente', nuevoCliente.as_view(), name="nuevoCliente"),
    path('facturas/nuevaFactura', nuevaFactura, name="nuevaFactura"),
    path('clientes/editarCliente/<int:pk>', editarCliente.as_view(), name="editarCliente"),
    path('facturas/editarFactura/<int:id>', nuevaFactura, name="editarFactura"),
    path('clientes/estadoCliente/<int:idCliente>', estadoCliente, name="estadoCliente"),
    path('facturas/borrarDetalleFactura/<int:id>', borrarDetalleFactura, name="borrarDetalleFactura"),
    path('facturas/imprimirFactura/<int:id>', imprimirFactura, name="imprimirFactura"),
]
