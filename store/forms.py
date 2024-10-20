from typing import Any, Mapping
from django import forms
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList
from .models import Books
from datetime import datetime

class BookForm(forms.ModelForm):

    class Meta:
        model = Books
        fields=['name', 'description', 'price']

    def save(self, *args, **kwargs):
        # Bookクラスのインスタンスをobjにセットする
        obj = super(BookForm, self).save(commit=False)
        obj.create_at=datetime.now()
        obj.update_at=datetime.now()
        obj.save()
        return obj

class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Books
        fields=['name', 'description', 'price']

    def save(self, *args, **kwargs):
        # Bookクラスのインスタンスをobjにセットする
        obj = super(BookUpdateForm, self).save(commit=False)
    ##    obj.create_at=datetime.now()
        obj.update_at=datetime.now()
        obj.save()
        return obj  

class BookPForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix=' '
    price=forms.IntegerField(label='価格')
