from datetime import datetime

from django.forms import *

from core.erp.models import  Product, Client, Sale

from decimal import Decimal

class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),

        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON() #que devuelva un JSON de lo guardado
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    def clean(self):
        cleaned_data = super().clean()
        cost = float(cleaned_data.get("cost"))
        pvp = float(cleaned_data.get("pvp"))

        min = cost+cost*0.2
        if  pvp < min:
            msg = "El precio de venta no puede ser menor o igual al costo mas ganancia (20%) = "+str(min)
            self.add_error('cost', msg)

class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'names': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'surnames': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'dni': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dni',
                }
            ),
            'date_birthday': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': "datetime.now().strftime('%Y-%m-%d')",
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_birthday',
                    'data-target': '#date_birthday',
                    'data-toggle': 'datetimepicker',
                }
            ),
            'address': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),
            'gender': Select()
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # def clean(self):
    #     cleaned = super().clean()
    #     if len(cleaned['name']) <= 50:
    #         raise forms.ValidationError('Validacion xxx')
    #         # self.add_error('name', 'Le faltan caracteres')
    #     return cleaned

class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
        # combo cliente
         self.fields['cli'].widget.attrs['autofocus'] = True


    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'cli': Select(attrs={
                'class': 'custom-select ',
                #'style': 'width: 100%',
            }),
            'date_joined': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': "datetime.now().strftime('%Y-%m-%d')",
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_joined',
                    'data-target': '#date_joined',
                    'data-toggle': 'datetimepicker',
                }
            ),
            'iva': TextInput(attrs = {
                'class': 'form-control',
            }),
            'subtotal': TextInput(attrs = {
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })

        }
class FilterForm(Form):
    # select numero de filas a mostrar
    filter_rows = CharField(widget=Select(attrs={
        'class': 'form-control select2',
        'autocomplete': 'off',
    }))
    # input para buscar
    srch = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off',
        # si se le da click se seleccione el contenido
        'onClick': 'this.setSelectionRange(0, this.value.length)',
        'placeholder': 'Buscar',
    }))