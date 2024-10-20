from django.shortcuts import render
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView, View
from .forms import RegistForm, UserLoginForm

class HomeView(TemplateView):	 
    template_name = 'accounts/home.html'	

class RegistUserView(CreateView):	 
    template_name = 'accounts/regist.html'	
    form_class = RegistForm	

class UserLoginView(FormView):
    template_name = 'accounts/user_login.html'
    form_class = UserLoginForm 

class UserLogoutView(View):
    pass
