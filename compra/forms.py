from django import forms
from .models import Proveedor, Compra

class ProveedorForm(forms.ModelForm):
    correo = forms.EmailField(max_length=254)

    class Meta:
        model = Proveedor
        exclude = ['fechaCreacion', 'fechaModificacion', 'usuarioCrea', 'usuarioModifica']
        widget = {'descripcion': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class CompraForm(forms.ModelForm):
    fechaCompra = forms.DateInput()
    fechaFactura = forms.DateInput()

    class Meta:
        model = Compra
        fields = ['proveedor', 'fechaCompra', 'observacion', 'numFactura', 'fechaFactura', 'subTotal', 'descuento', 'total']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['fechaCompra'].widget.attrs['readonly'] = True
        self.fields['fechaFactura'].widget.attrs['readonly'] = True
        self.fields['subTotal'].widget.attrs['readonly'] = True
        self.fields['descuento'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True
