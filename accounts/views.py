from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView, View
from .forms import RegistForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout	
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView

class HomeView(TemplateView):	 
    template_name = 'accounts/home.html'	

class RegistUserView(CreateView):	 
    template_name = 'accounts/regist.html'	
    form_class = RegistForm	

'''
class UserLoginView(FormView):
    template_name = 'accounts/user_login.html'
    form_class = UserLoginForm 

    def post(self, request, *args, **kwargs):
        if "btn_home" in request.POST:
            return redirect('accounts:home')

        form=UserLoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
        
            user = authenticate(email=email, password=password) 
            if user is not None and user.is_active:
                login(request, user)
                return redirect('accounts:home')

            # 認証エラーの場合、フォームにエラーメッセージを追加
            form.add_error(None, ValidationError('ユーザ名かパスワードが正しくありません'))

        # エラーがある場合はform_invalidを呼び出す
        return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        # フォームのデータを使ってcontextに追加できる
        context['email'] = form.cleaned_data.get('email', '')
        context['password'] = ''
        return self.render_to_response(context)

class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:user_login')
'''

class UserView(TemplateView):
    template_name = 'accounts/user.html'

    @method_decorator(login_required)	
    def dispatch(self, *args, **kwargs):	
        return super().dispatch(*args, **kwargs)
    

'''
@method_decorator(login_required, name='dispatch')
class UserView(TemplateView):
    template_name = 'accounts/user.html'

    def dispatch(self, *args, **kwargs):	
        return super().dispatch(*args, **kwargs)
'''

'''
class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/user.html'

    def dispatch(self, *args, **kwargs):	
        return super().dispatch(*args, **kwargs)
'''

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    authentication_form = UserLoginForm 

    def post(self, request, *args, **kwargs):
        if "btn_home" in request.POST:
            return redirect('accounts:home')
        # 通常のログイン処理を行う
        return super().post(request, *args, **kwargs)

class UserLogoutView(LogoutView):
    pass