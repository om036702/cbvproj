from django import forms
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