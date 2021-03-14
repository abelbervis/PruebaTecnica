import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from core.erp.forms import SaleForm, ClientForm, ProductForm,  FilterForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from core.erp.models import Sale, Product, DetSale, Client

from django.db.models import Q

# xhtmlpdf2
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


class SaleListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Sale
    template_name = 'sale/list.html'
    permission_required = 'view_sale'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        '''try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Sale.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in DetSale.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        '''
        try:
            action = request.POST['action']
            if action == 'getcount':
                if request.POST['search'] == "":
                    # si no es una busqueda entonces retornar total de elementos de la tabla
                    data['count'] = str(Sale.objects.count())
                else:
                    # sino que devuelva el total de elementos que tiene la consulta
                    search = request.POST['search']
                    s = Sale.objects.filter(Q(cli__names__icontains=search) | Q(cli__surnames__icontains=search) | Q(cli__dni__icontains=search))
                    data['count'] = str(s.count())
            elif action == 'searchdatapagination':
                data = []
                start_page = int(request.POST['start_page'])
                end_page = int(request.POST['end_page'])
                search = request.POST['search']
                if search == "":
                    # devuelva un json con datos de la pagina
                    for i in Sale.objects.all()[start_page:end_page]:
                        data.append(i.toJSON())
                else:
                    # devuelva un json con datos de la busqueda
                    for i in Sale.objects.filter(Q(cli__names__icontains=search) | Q(cli__surnames__icontains=search) | Q(cli__dni__icontains=search))[start_page:end_page]:
                        data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

        print('data al final SaleListView: ')
        print(data)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('erp:sale_create')
        context['list_url'] = reverse_lazy('erp:sale_list')
        context['entity'] = 'Ventas'
        context['frmClient'] = ClientForm()
        # form filter
        context['FilterForm'] = FilterForm()
        return context

class SaleCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('erp:sale_list')
    permission_required = 'add_sale'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print("-----------------------------------------------------------------------------")
            print(request.POST)
            if action == 'search_products':
                data = []
                prods = Product.objects.filter(Q(Q(name__icontains=request.POST['term'])|Q(code__icontains=request.POST['term'])) & Q(active__contains=0))[0:10]
                for i in prods:
                    item = i.toJSON()
                    #item['value'] = i.name
                    #select2 usa id y text
                    item['text'] = i.name
                    data.append(item)
            elif action == 'search_clients':
                data = []
                cls = Client.objects.filter(Q(names__icontains=request.POST['term']) | Q(surnames__icontains=request.POST['term']) | Q(dni__icontains=request.POST['term']))[0:10]
                for i in cls:
                    item = i.toJSON()
                    #item['value'] = i.name
                    #select2 usa id y text
                    item['text'] = i.surnames
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    sale = Sale()
                    sale.date_joined = vents['date_joined']
                    sale.cli_id = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()
                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()

                    # envio el id para imprimir pdf
                    data = {'id': sale.id}
            elif action == 'create_client':
                with transaction.atomic():
                    #paso lo que envia al formulario
                    frmClient = ClientForm(request.POST)
                    data = frmClient.save()
            elif action == 'create_product':
                with transaction.atomic():
                    #paso lo que envia al formulario
                    frmProduct = ProductForm(request.POST)
                    data = frmProduct.save() #sobrescritura de save devuelve JSON
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        print(data)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        context['frmClient'] = ClientForm()
        context['frmProduct'] = ProductForm()

        return context

class SaleUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('erp:sale_list')
    permission_required = 'change_sale'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Product.objects.filter(Q(Q(name__icontains=request.POST['term'])|Q(code__icontains=request.POST['term'])) & Q(active__contains=0))[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.name
                    data.append(item)
            elif action == 'search_clients':
                data = []
                cls = Client.objects.filter(Q(names__icontains=request.POST['term']) | Q(surnames__icontains=request.POST['term']) | Q(dni__icontains=request.POST['term']))[0:10]
                for i in cls:
                    item = i.toJSON()
                    item['text'] = i.surnames
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    # obtiene el objeto con que se este trabajando y asi poder actualizar
                    sale = self.get_object()
                    sale.date_joined = vents['date_joined']
                    sale.cli_id = vents['cli']
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.save()
                    #borro el detalle
                    sale.detsale_set.all().delete()
                    for i in vents['products']:
                        det = DetSale()
                        det.sale_id = sale.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.price = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    # envio el id para imprimir pdf
                    data = {'id': sale.id}
            elif action == 'create_client':
                with transaction.atomic():
                    #paso lo que envia al formulario
                    frmClient = ClientForm(request.POST)
                    data = frmClient.save()
            elif action == 'create_product':
                with transaction.atomic():
                    #paso lo que envia al formulario
                    frmProduct = ProductForm(request.POST)
                    data = frmProduct.save() #sobrescritura de save devuelve JSON
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_products(self):
        data = []
        try:
            for i in DetSale.objects.filter(sale_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cant
                item['price'] = format(i.price, '.2f')
                data.append(item)
        except:
            pass
        return data


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_products())
        context['frmClient'] = ClientForm()
        context['frmProduct'] = ProductForm()
        return context

class SaleDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Sale
    template_name = 'sale/delete.html'
    success_url = reverse_lazy('erp:sale_list')
    permission_required = 'delete_sale'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        return context

# vista para generar PDF
class SaleInvoicePdfView(LoginRequiredMixin, View):


    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """

        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        print("exe: " + sUrl + mUrl)

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    # sobrescribo el metodo get
    def get(self, request, *args, **kwargs):
        try:
            # find the template and render it.
            template = get_template('sale/invoice.html')
            mySale = Sale.objects.get(pk=self.kwargs['pk'])
            #se le pasaal template
            context = {
                'sale': mySale,
                'comp': {'name':'Bervis S.A','ruc':'99999999999','address':'Leon Nicaragua'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png'),
                'iva_porc': {'iva': mySale.iva/mySale.subtotal*100}
            }
            html = template.render(context)
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            # esta linea hace que se descargue el archivo
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"'

            # create a pdf
            pisa_status = pisa.CreatePDF(
                html, dest=response,
                link_callback = self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:sale_list'))

