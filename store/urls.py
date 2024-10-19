from django.urls import path
from .views import IndexView

app_name = 'library'
urlpatterns = [
    path('index/',IndexView.as_view(), name='index'),
]
