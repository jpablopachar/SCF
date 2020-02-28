from django.urls import path
from .views import listarCategorias, listarSubcategorias, listarMarcas, listarUnidadesMedida, listarProductos, nuevaCategoria, nuevaSubcategoria, nuevaMarca, nuevaUnidadMedida, nuevoProducto, editarCategoria, editarSubcategoria, editarMarca, editarUnidadMedida, editarProducto, eliminarCategoria, eliminarSubcategoria, inactivarMarca, inactivarUnidadMedida, inactivarProducto

urlpatterns = [
    path('categorias/', listarCategorias.as_view(), name='listaCategorias'),
    path('subcategorias/', listarSubcategorias.as_view(), name='listaSubcategorias'),
    path('marcas/', listarMarcas.as_view(), name='listaMarcas'),
    path('unidadesMedida/', listarUnidadesMedida.as_view(), name='listaUnidadesMedida'),
    path('productos/', listarProductos.as_view(), name='listaProductos'),
    path('categorias/nueva', nuevaCategoria.as_view(), name='nuevaCategoria'),
    path('subcategorias/nueva', nuevaSubcategoria.as_view(), name='nuevaSubcategoria'),
    path('marcas/nueva', nuevaMarca.as_view(), name='nuevaMarca'),
    path('unidadesMedida/nueva', nuevaUnidadMedida.as_view(), name='nuevaUnidadMedida'),
    path('productos/nuevo', nuevoProducto.as_view(), name='nuevoProducto'),
    path('categorias/editar/<int:pk>', editarCategoria.as_view(), name='editarCategoria'),
    path('subcategorias/editar/<int:pk>', editarSubcategoria.as_view(), name='editarSubcategoria'),
    path('marcas/editar/<int:pk>', editarMarca.as_view(), name='editarMarca'),
    path('unidadesMedida/editar/<int:pk>', editarUnidadMedida.as_view(), name='editarUnidadMedida'),
    path('productos/editar/<int:pk>', editarProducto.as_view(), name='editarProducto'),
    path('categorias/eliminar/<int:pk>', eliminarCategoria.as_view(), name='eliminarCategoria'),
    path('subcategorias/eliminar/<int:pk>', eliminarSubcategoria.as_view(), name='eliminarSubcategoria'),
    path('marcas/inactivar/<int:id>', inactivarMarca, name='inactivarMarca'),
    path('unidadesMedida/inactivar/<int:id>', inactivarUnidadMedida, name='inactivarUnidadMedida'),
    path('producto/inactivar/<int:id>', inactivarProducto, name='inactivarProducto')
]
