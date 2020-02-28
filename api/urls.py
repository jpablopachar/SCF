from django.urls import path
from .views import listarProductos, detalleProducto


urlpatterns = [
    path('productos/', listarProductos.as_view(), name="listaProductos"),
    path('productos/<str:codigo>', detalleProducto.as_view(), name="detalleProducto"),
]