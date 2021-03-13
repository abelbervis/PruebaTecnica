from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.erp.models import Sale, Product, DetSale


class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_graph_sales_year_months':
                data = {
                    'name': 'Porcentaje de venta',
                    'showInLegend': False,
                    'colorByPoint': True,
                    'data': self.get_graph_sales_year_months(),
                }
            elif action == 'get_graph_sales_products_year_month':
                data = {
                    'name': 'Porcentaje de venta',
                    'colorByPoint': True,
                    'data': self.get_graph_sales_products_year_month(),
                }
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_graph_sales_year_months(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                total = Sale.objects.filter(date_joined__year=year, date_joined__month=m).aggregate(r=Coalesce(Sum('total'), 0)).get('r')
                if total > 0:
                    data.append(float(total))
            return data
        except:
            pass
        return data

    def get_graph_sales_products_year_month(self):
        data = []
        try:
            year = datetime.now().year
            month = datetime.now().month
            for p in Product.objects.all():
                total = DetSale.objects.filter(sale__date_joined__year=year, sale__date_joined__month=month, prod_id=p.id).aggregate(
                    r=Coalesce(Sum('subtotal'), 0)).get('r')
                if total > 0:
                    data.append({
                        'name': p.name,
                        'y': float(total),
                    })
            return data
        except:
            pass
        return data

    def get_name_month(self, n_month):
        name = ''
        if n_month == 1:
            name = 'Enero'
        elif n_month == 2:
            name = 'Febrero'
        elif n_month == 3:
            name = 'Marzo'
        elif n_month == 4:
            name = 'Abril'
        elif n_month == 5:
            name = 'Mayo'
        elif n_month == 6:
            name = 'Junio'
        elif n_month == 7:
            name = 'Julio'
        elif n_month == 8:
            name = 'Agosto'
        elif n_month == 9:
            name = 'Septiembre'
        elif n_month == 10:
            name = 'Octubre'
        elif n_month == 11:
            name = 'Noviembre'
        elif n_month == 12:
            name = 'Diciembre'
        return  name


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        context['graph_sales_year_months'] = self.get_graph_sales_year_months()
        context['year'] = datetime.now().year
        context['month'] = self.get_name_month(datetime.now().month)
        return context
