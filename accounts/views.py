from django.shortcuts import render
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView, View
from .forms import RegistForm

class HomeView(TemplateView):               #<--　ホーム画面（TemplateViewを継承） 
    template_name = 'accounts/home.html'    #<--　テンプレートで表示したい画面

class RegistUserView(CreateView):           #<--　登録用画面（CreateViewを継承） 
    template_name = 'accounts/regist.html'  #<--　テンプレートで表示したい画面
    form_class = RegistForm                 #<--　使用するフォームクラス

class UserLoginView(FormView):              #<--　あとで記述
    pass

class UserLogoutView(View):                 #<--　あとで記述
    pass
