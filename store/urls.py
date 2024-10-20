from django.urls import path
from .views import (IndexView, HomeView, BookDetailView, BookListView, BookCreateView, BookUpdateView, BookDeleteView, BookPView, BookRedirectView)
# from django.views.generic.base import TemplateView
from django.views.generic.base import RedirectView

app_name = 'store'
urlpatterns = [
    path('index/',IndexView.as_view(), name='index'),
    # path('home/',HomeView.as_view(), name='home'),
    path('home/<name>',HomeView.as_view(), name='home'),
    path('detail_book/<int:pk>',BookDetailView.as_view(), name='detail_book'),
    path('list_book/',BookListView.as_view(), name='list_book'),    
    path('list_book/<name>',BookListView.as_view(), name='list_book'),    
    path('add_book/',BookCreateView.as_view(), name='add_book'),    
    path('edit_book/<int:pk>',BookUpdateView.as_view(), name='edit_book'),
    path('delete_book/<int:pk>',BookDeleteView.as_view(), name='delete_book'),
    path('bookprice/',BookPView.as_view(), name='bookprice'),
    path('ttc/',RedirectView.as_view(url='https://tec.ttc.ac.jp/departments/it-game-web/iot-ai/')),
    path('book_redirect_view/',BookRedirectView.as_view(), name='book_redirect_view'),
    path('book_redirect_view/<int:pk>',BookRedirectView.as_view(), name='book_redirect_view'),
]
