from django.urls import path
from .views import (IndexView, HomeView)
# from django.views.generic.base import TemplateView

app_name = 'store'
urlpatterns = [
    path('index/',IndexView.as_view(), name='index'),
    path('home/',HomeView.as_view(), name='home'),
]
