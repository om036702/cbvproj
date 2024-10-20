from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import(
    View,TemplateView,
)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import(
    CreateView, UpdateView, DeleteView,
    FormView,
)
from django.urls import reverse_lazy
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

class BookCreateView(CreateView):
    model=Books
    fields=['name', 'description', 'price']
    template_name='add_book.html'
    ##  success_url=reverse_lazy('store:list_book')

    def form_valid(self, form):
        form.instance.create_at=datetime.now()
        form.instance.update_at=datetime.now()
        return super().form_valid(form)

    def get_initial(self, **kwargs):
        initial=super(BookCreateView, self).get_initial(**kwargs)
        initial['name']='sample本'
        initial['description']='sample本の説明'
        initial['price']=0
        return initial

class BookUpdateView(UpdateView):
    model=Books
    template_name='update_book.html'
    form_class=forms.BookUpdateForm

    def get_success_url(self):
        return reverse_lazy('store:edit_book',kwargs={'pk':self.object.id})

class BookDeleteView(DeleteView):
    model=Books
    template_name='delete_book.html'
    success_url=reverse_lazy('store:list_book')

class BookPView(FormView):
    form_class=forms.BookPForm
    template_name='book_price.html'

    def get_initial(self) -> dict[str, Any]:
        initial=super(BookPView, self).get_initial()
        initial['price']=0
        return initial

    def form_valid(self, form):
        c_price=form.cleaned_data.get('price')
        tax=int(c_price/11)
        hontai=c_price - tax

        context={'form':form, 'hontai': hontai, 'tax': tax}
        return render(self.request, self.template_name, context)
