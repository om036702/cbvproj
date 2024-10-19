from django.urls import path
from .views import (IndexView, HomeView, BookDetailView)
# from django.views.generic.base import TemplateView

app_name = 'store'
urlpatterns = [
    path('index/',IndexView.as_view(), name='index'),
    # path('home/',HomeView.as_view(), name='home'),
    path('home/<name>',HomeView.as_view(), name='home'),
    path('detail_book/<int:pk>',BookDetailView.as_view(), name='detail_book'),
]
