Djangoの ValidationError をフォームに表示させるためには、form.add_error() を使用してフォームフィールドにエラーメッセージを追加するのが一般的です。その後、レンダリング時にフォーム全体が自動的にエラーメッセージを表示します。

次に、ValidationError が発生したときに、そのエラーメッセージをログイン画面に表示する方法を示します。

1. views.py の修正

ValidationError をフォームに追加し、エラーメッセージをテンプレートに表示できるようにします。

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import UserLoginForm
from django.core.exceptions import ValidationError

class UserLoginView(FormView):
    template_name = 'accounts/user_login.html'
    form_class = UserLoginForm

    def post(self, request, *args, **kwargs):
        if "btn_home" in request.POST:
            return redirect('accounts:home')

        form = self.get_form(self.form_class)  # フォームを取得
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(email=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('accounts:home')

            # 認証エラーの場合、フォームにエラーメッセージを追加
            form.add_error(None, ValidationError('ユーザ名かパスワードが正しくありません'))

        # エラーがある場合、元のページにフォームとエラーメッセージを返す
        return self.form_invalid(form)

2. user_login.html の修正

テンプレートには、フォームのエラーメッセージが自動的に表示されるため、特に変更を加える必要はありません。ただし、エラーメッセージが適切に表示されることを確認するために、以下のようにフォームをレンダリングします。

{% extends 'accounts/base.html' %}
{% block content %}
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}  <!-- フォームに含まれるエラーメッセージを表示 -->
    <input type="hidden" name="next" value="{{ request.GET.next }}">
    <input type="submit" value="ログイン">
    <input type="submit" name="btn_home" value="ホーム" novalidate>
</form>
{% endblock %}

動作の流れ

	•	form.is_valid() をチェックした後、認証が失敗した場合に form.add_error() を使ってエラーメッセージを追加します。
	•	その後、self.form_invalid(form) を呼び出してエラーメッセージ付きのフォームを再度表示します。
	•	テンプレート内の {{ form.as_p }} がエラーメッセージと一緒にフォームをレンダリングします。

これにより、認証に失敗した場合にログイン画面にエラーメッセージが表示されます。


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
上記のコードを form_invalid() メソッドに置き換えることで、フォームが無効な状態で再レンダリングされる際にエラーメッセージが正しく表示されるようにできます。context の手動設定は不要で、form_invalid() を呼び出すと Django が自動的にフォームに関するコンテキストデータを生成してくれます。

もし、手動で email や password フィールドのデータを引き渡したい場合、context を更新する必要がある場合のみ対応すればよいです。

次のようにコードを修正できます：

修正後の views.py コード

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import UserLoginForm
from django.core.exceptions import ValidationError

class UserLoginView(FormView):
    template_name = 'accounts/user_login.html'
    form_class = UserLoginForm

    def post(self, request, *args, **kwargs):
        if "btn_home" in request.POST:
            return redirect('accounts:home')

        form = self.get_form(self.form_class)  # フォームを取得
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(email=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('accounts:home')

            # 認証エラーの場合、フォームにエラーメッセージを追加
            form.add_error(None, ValidationError('ユーザ名かパスワードが正しくありません'))

        # エラーがある場合はform_invalidを呼び出す
        return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        # フォームのデータを使ってcontextに追加できる
        context['email'] = form.cleaned_data.get('email', '')
        context['password'] = ''
        return self.render_to_response(context)

変更点のポイント

	1.	form_invalid() メソッドの追加:
フォームが無効なときの処理を form_invalid() メソッド内に移動しました。このメソッドでは、手動で context を設定し、エラーメッセージやフォームデータを含めて画面を再表示します。
	2.	context の設定:
context を設定するときに、self.get_context_data(form=form) を使うことで、Django が自動的にフォームデータをコンテキストに追加します。加えて、必要なフィールド（この場合、email や空の password）を手動で追加しています。

動作の流れ

	•	認証エラー時に、エラーメッセージをフォームに追加して form_invalid(form) を呼び出します。
	•	form_invalid() でエラーメッセージ付きのフォームとデータを再レンダリングし、テンプレートに表示します。