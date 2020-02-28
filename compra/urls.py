from django.urls import path, include
from .views import listarProveedores, listarCompras, nuevoProveedor, nuevaCompra, editarProveedor, inactivarProveedor, eliminarDetalleCompra
from .reportes import reporteCompras, reporteCompra

urlpatterns = [
    path('proveedores/', listarProveedores.as_view(), name="listaProveedores"),
    path('compras/', listarCompras.as_view(), name="listaCompras"),
    path('proveedores/nuevo', nuevoProveedor.as_view(), name="nuevoProveedor"),
    path('compras/nuevo', nuevaCompra, name="nuevaCompra"),
    path('proveedores/editar/<int:pk>', editarProveedor.as_view(), name="editarProveedor"),
    path('compras/editar/<int:idCompra>', nuevaCompra, name="editarCompra"),
    path('proveedores/inactivar/<int:id>', inactivarProveedor, name="inactivarProveedor"),
    path('compras/<int:idCompra>/eliminar/<int:pk>', eliminarDetalleCompra.as_view(), name="eliminarDetalleCompra"),
    path('compras/imprimirCompras', reporteCompras, name="imprimirCompras"),
    path('compras/<int:idCompra>/imprimir', reporteCompra, name="imprimirCompra"),
]
