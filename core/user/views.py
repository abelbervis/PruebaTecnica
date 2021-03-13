from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, FormView

from core.erp.forms import FilterForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.user.forms import UserForm, UserProfileForm
from core.user.models import User


class UserListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = User
    template_name = 'user/list.html'
    permission_required = 'view_user'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self,request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'getcount':
                if request.POST['search'] == "":
                    # si no es una busqueda entonces retornar total de elementos de la tabla
                    data['count'] = str(User.objects.count())
                else:
                    # sino que devuelva el total de elementos que tiene la consulta
                    search = request.POST['search']
                    c = User.objects.filter(
                        Q(username__icontains=search) | Q(first_name__icontains=search) |Q(last_name__icontains=search) | Q(email__icontains=search))
                    data['count'] = str(c.count())
            elif action == 'searchdatapagination':
                data = []
                start_page = int(request.POST['start_page'])
                end_page = int(request.POST['end_page'])
                search = request.POST['search']
                if search == "":
                    # devuelva un json con datos de la pagina
                    for i in User.objects.all()[start_page:end_page]:
                        data.append(i.toJSON())
                else:
                    # devuelva un json con datos de la busqueda
                    for i in User.objects.filter(
                            Q(username__icontains=search) | Q(first_name__icontains=search) |Q(last_name__icontains=search) | Q(email__icontains=search))[
                             start_page:end_page]:
                        data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Usuarios'
        context['create_url'] = reverse_lazy('user:user_create')
        context['list_url'] = reverse_lazy('user:user_list')
        context['entity'] = 'Usuarios'
        # form filter
        context['FilterForm'] = FilterForm()
        return context

class UserCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('user:user_list')
    permission_required = 'change_user'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class UserUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('user:user_list')
    permission_required = 'add_user'
    url_redirect = success_url


    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de un usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class UserDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('user:user_list')
    permission_required = 'delete_user'
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
        context['title'] = 'Eliminación de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        return context

class UserChangeGroup(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            request.session['group'] = Group.objects.get(pk=self.kwargs['pk'])
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:dashboard'))

class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'user/profile.html'
    success_url = reverse_lazy('erp:dashboard')


    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de perfil'
        context['entity'] = 'Perfil'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class UserChangePasswordView(LoginRequiredMixin, FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'user/profile.html'
    success_url = reverse_lazy('login')


    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs['placeholder']= 'ingrese su contrasena actual'
        form.fields['new_password1'].widget.attrs['placeholder'] = 'ingrese la contrasena nueva'
        form.fields['new_password2'].widget.attrs['placeholder'] = 'repita su contrasena nueva'
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    #para que no cierre sesion al cambiar la contrasena
                    update_session_auth_hash(request, form.user)
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de password'
        context['entity'] = 'Password'
        context['list_url'] = self.success_url
        context['action'] = 'edit'

        return context

