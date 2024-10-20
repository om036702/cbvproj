from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic.base import(
    View,TemplateView,
)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Books
from . import forms
from datetime import datetime

class IndexView(View):
    def get(self, request, *args, **kwargs):
        book_form=forms.BookForm()
        return render(request, 'index.html', context={'book_form':book_form,})

    def post(self, request, *args, **kwargs):
        book_form = forms.BookForm(request.POST or None)
        if book_form.is_valid():
            book_form.save()
            return render(request, 'index.html', context={'book_form':book_form,})

class HomeView(TemplateView):
    template_name='home.html'
    def get_context_data(self, **kwargs: Any):
        context=super().get_context_data(**kwargs)
        context['name']=kwargs.get('name')
        context['time']=datetime.now()
        return context

class BookDetailView(DetailView):
    model=Books
    template_name='book.html'

class BookListView(ListView):
    model=Books
    template_name='book_list.html'

    def get_queryset(self):
        qs=super(BookListView, self).get_queryset()
        # 絞り込み
        if 'name' in self.kwargs:
            qs=qs.filter(name__startswith=self.kwargs['name'])
        qs=qs.order_by('-id')
        return qs