from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from bases.views import SinPrivilegios
from .models import Categoria, SubCategoria, Marca, UnidadMedida, Producto
from .forms import CategoriaForm, SubcategoriaForm, MarcaForm, UnidadMedidaForm, ProductoForm


class listarCategorias(SinPrivilegios, generic.ListView):
    permission_required = "inventario.view_categoria"
    model = Categoria
    template_name = "inventario/listaCategorias.html"
    context_object_name = "categorias"


class listarSubcategorias(SinPrivilegios, generic.ListView):
    permission_required = "inventario.view_subcategoria"
    model = SubCategoria
    template_name = "inventario/listaSubcategorias.html"
    context_object_name = "subcategorias"


class listarMarcas(SinPrivilegios, generic.ListView):
    permission_required = "inventario.view_marca"
    model = Marca
    template_name = "inventario/listaMarcas.html"
    context_object_name = "marcas"


class listarUnidadesMedida(SinPrivilegios, generic.ListView):
    permission_required = "inventario.view_unidadMedida"
    model = UnidadMedida
    template_name = "inventario/listaUnidadesMedida.html"
    context_object_name = "unidadesMedida"


class listarProductos(SinPrivilegios, generic.ListView):
    permission_required = "inventario.view_producto"
    model = Producto
    template_name = "inventario/listaProductos.html"
    context_object_name = "productos"


class nuevaCategoria(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    model = Categoria
    template_name = "inventario/formCategoria.html"
    context_object_name = "categoria"
    form_class = CategoriaForm
    success_url = reverse_lazy("inventario:listaCategorias")
    success_message = "La categoría se ha creado correctamente"
    permission_required = "inventario.add_categoria"

    def form_valid(self, form):
        form.instance.usuarioCrea = self.request.user

        return super().form_valid(form)


class nuevaSubcategoria(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    model = SubCategoria
    template_name = "inventario/formSubcategoria.html"
    context_object_name = "subcategoria"
    form_class = SubcategoriaForm
    success_url = reverse_lazy("inventario:listaSubcategorias")
    success_message = "La subcategoría se ha creado correctamente"
    permission_required = "inventario.add_subcategoria"

    def form_valid(self, form):
        form.instance.usuarioCrea = self.request.user

        return super().form_valid(form)


class nuevaMarca(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    model = Marca
    template_name = "inventario/formMarca.html"
    context_object_name = "marca"
    form_class = MarcaForm
    success_url = reverse_lazy("inventario:listaMarcas")
    success_message = "La marca se ha creado correctamente"
    permission_required = "inventario.add_marca"

    def form_valid(self, form):
        form.instance.usuarioCrea = self.request.user

        return super().form_valid(form)


class nuevaUnidadMedida(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    model = UnidadMedida
    template_name = "inventario/formUnidadMedida.html"
    context_object_name = "unidadMedida"
    form_class = UnidadMedidaForm
    success_url = reverse_lazy("inventario:listaUnidadesMedida")
    success_message = "La unidad de medida se ha creado correctamente"
    permission_required = "inventario.add_unidadMedida"

    def form_valid(self, form):
        form.instance.usuarioCrea = self.request.user

        return super().form_valid(form)


class nuevoProducto(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
    model = Producto
    template_name = "inventario/formProducto.html"
    context_object_name = "producto"
    form_class = ProductoForm
    success_url = reverse_lazy("inventario:listaProductos")
    success_message = "El producto se ha creado correctamente"
    permission_required = "inventario.add_producto"

    def form_valid(self, form):
        form.instance.usuarioCrea = self.request.user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(nuevoProducto, self).get_context_data(**kwargs)
        context["categorias"] = Categoria.objects.all()
        context["subcategorias"] = SubCategoria.objects.all()

        return context


class editarCategoria(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    model = Categoria
    template_name = "inventario/formCategoria.html"
    context_object_name = "categoria"
    form_class = CategoriaForm
    success_url = reverse_lazy("inventario:listaCategorias")
    success_message = "La categoría ha sido actualizada correctamente"
    permission_required = "inventario.change_categoria"

    def form_valid(self, form):
        form.instance.usuarioModifica = self.request.user.id

        return super().form_valid(form)


class editarSubcategoria(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    model = SubCategoria
    template_name = "inventario/formSubcategoria.html"
    context_object_name = "subcategoria"
    form_class = SubcategoriaForm
    success_url = reverse_lazy("inventario:listaSubcategorias")
    success_message = "La subcategoría ha sido actualizada correctamente"
    permission_required = "inventario.change_subcategoria"

    def form_valid(self, form):
        form.instance.usuarioModifica = self.request.user.id

        return super().form_valid(form)


class editarMarca(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    model = Marca
    template_name = "inventario/formMarca.html"
    context_object_name = "marca"
    form_class = MarcaForm
    success_url = reverse_lazy("inventario:listaMarcas")
    success_message = "La marca ha sido actualizada correctamente"
    permission_required = "inventario.change_marca"

    def form_valid(self, form):
        form.instance.usuarioModifica = self.request.user.id

        return super().form_valid(form)


class editarUnidadMedida(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    model = UnidadMedida
    template_name = "inventario/formUnidadMedida.html"
    context_object_name = "unidadMedida"
    form_class = UnidadMedidaForm
    success_url = reverse_lazy("inventario:listaUnidadesMedida")
    success_message = "La unidad de medida ha sido actualizada correctamente"
    permission_required = "inventario.change_unidadMedida"

    def form_valid(self, form):
        form.instance.usuarioModifica = self.request.user.id

        return super().form_valid(form)


class editarProducto(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
    model = Producto
    template_name = "inventario/formProducto.html"
    context_object_name = "producto"
    form_class = ProductoForm
    success_url = reverse_lazy("inventario:listaProductos")
    success_message = "El producto ha sido actualizado correctamente"
    permission_required = "inventario.change_producto"

    def form_valid(self, form):
        form.instance.usuarioCrea = self.request.user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super(editarProducto, self).get_context_data(**kwargs)
        context["categorias"] = Categoria.objects.all()
        context["subcategorias"] = SubCategoria.objects.all()
        context["producto"] = Producto.objects.filter(pk=pk).first()

        return context


class eliminarCategoria(SuccessMessageMixin, SinPrivilegios, generic.DeleteView):
    model = Categoria
    template_name = 'inventario/eliminarCatalogo.html'
    context_object_name = 'obj'
    success_url = reverse_lazy("inventario:listaCategorias")
    success_message = "La categoría ha sido eliminada correctamente"
    permission_required = "inventario.delete_categoria"


class eliminarSubcategoria(SuccessMessageMixin, SinPrivilegios, generic.DeleteView):
    model = SubCategoria
    template_name = 'inventario/eliminarCatalogo.html'
    context_object_name = 'obj'
    success_url = reverse_lazy("inventario:listaSubcategorias")
    success_message = "La subcategoría ha sido eliminada correctamente"
    permission_required = "inventario.delete_subcategoria"


@login_required(login_url='/login/')
@permission_required('inventario.change_marca', login_url='bases:sinPrivilegios')
def inactivarMarca(request, id):
    marca = Marca.objects.filter(pk=id).first()
    contexto = {}
    template_name = "inventario/eliminarCatalogo.html"

    if not marca:
        return redirect("inventario:listaMarcas")

    if request.method == 'GET':
        contexto = {'obj': marca}

    if request.method == 'POST':
        marca.estado = False

        marca.save()
        messages.success(request, 'Marca inactivada')

        return redirect("inventario:listaMarcas")

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('inventario.change_unidadMarca', login_url='bases:sinPrivilegios')
def inactivarUnidadMedida(request, id):
    unidadMedida = UnidadMedida.objects.filter(pk=id).first()
    contexto = {}
    template_name = "inventario/eliminarCatalogo.html"

    if not unidadMedida:
        return redirect("inventario:listaUnidadesMedida")

    if request.method == 'GET':
        contexto = {'obj': unidadMedida}

    if request.method == 'POST':
        unidadMedida.estado = False

        unidadMedida.save()

        return redirect("inventario:listaUnidadesMedida")

    return render(request, template_name, contexto)


@login_required(login_url='/login/')
@permission_required('inventario.change_producto', login_url='bases:sinPrivilegios')
def inactivarProducto(request, id):
    producto = Producto.objects.filter(pk=id).first()
    contexto = {}
    template_name = "inventario/eliminarCatalogo.html"

    if not producto:
        return redirect("inventario:listaProductos")

    if request.method == 'GET':
        contexto = {'obj': producto}

    if request.method == 'POST':
        producto.estado = False

        producto.save()

        return redirect("inventario:listaProductos")

    return render(request, template_name, contexto)
