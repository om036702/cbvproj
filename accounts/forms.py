from django import forms
from .models import Users
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class RegistForm(forms.ModelForm):  #<-- 画面で登録のための項目を指定
    username = forms.CharField(label='名前', widget=forms.TextInput(attrs={'class':'form-control'}))
    age = forms.IntegerField(label='年齢', min_value=0, widget=forms.NumberInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='メールアドレス',widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:                     #<-- ResistFormとUsersを紐づける
        model = Users
        fields = ['username', 'age', 'email', 'password']

    def clean_password(self):
        user = super().save(commit=False)
        pwd=self.cleaned_data['password']
        try:
            validate_password(pwd, user)
        except ValidationError as e:
            self.add_error(None,e)
            raise forms.ValidationError('Password error')
        return pwd

    def save(self, commit=False):	
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])	
        user.save()	
        return user
