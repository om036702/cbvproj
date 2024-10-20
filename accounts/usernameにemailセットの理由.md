Djangoのデフォルト認証システムでは、ログイン時にusernameフィールドを使ってユーザーを認証しますが、UserLoginFormでusernameフィールドをEmailFieldに置き換えている場合、以下のような理由で正常に動作します。

理由

	1.	UserLoginFormのカスタマイズ:
AuthenticationFormでusernameはログインのためのユーザー識別情報を受け取るフィールドです。usernameというフィールド名はDjangoの認証システムで固定されており、デフォルトではユーザー名（username）が入力されることを期待します。しかし、usernameフィールドをEmailFieldに置き換えることで、Djangoはそのフィールドにメールアドレスが入力されると想定します。
つまり、フォーム側ではラベルやフィールドの型がどうであれ、フィールド名がusernameであればDjangoの認証システムはそのフィールドを使って認証処理を実行します。ここで、usernameフィールドにメールアドレスを入力しているため、認証システムはそれをユーザー名として扱い、認証を試みます。
	2.	AUTHENTICATION_BACKENDSの設定:
Djangoの認証システムは、AUTHENTICATION_BACKENDSという設定で、どのような情報を使ってユーザーを認証するかを制御します。例えば、デフォルトではdjango.contrib.auth.backends.ModelBackendが使われ、usernameフィールド（ここではメールアドレス）をもとにユーザーを検索します。もしDjangoがデフォルトでユーザー名ではなくメールアドレスを使ってログインを認証するよう設定されている場合、このようなカスタマイズは問題なく動作します。
メールアドレスで認証したい場合は、AUTHENTICATION_BACKENDSを次のように設定することが一般的です。これにより、メールアドレスを使って認証できます。

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # デフォルトのバックエンド
)

Djangoではこの設定を変更することで、usernameやemailなど、どのフィールドを使ってログインするかを決定します。

	3.	ユーザーモデルの変更:
Djangoのカスタムユーザーモデルを使用している場合、USERNAME_FIELDをemailに設定しておけば、Djangoはemailフィールドをユーザー識別情報として扱います。これにより、ユーザー名の代わりにメールアドレスでログインできます。

from django.contrib.auth.models import AbstractBaseUser

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'  # 認証に使うフィールドをemailに変更

こうすることで、usernameというフィールド名を使っていても、実際にはメールアドレスで認証が行われる仕組みになります。

結論

	•	フィールド名としてusernameを使っているが、その中身にメールアドレスが入力されているため、認証システムはそれを使ってユーザーを認証します。
	•	USERNAME_FIELDやAUTHENTICATION_BACKENDSでのカスタマイズが有効であれば、usernameに実際にはメールアドレスがセットされ、それを基にログイン処理が行われるようになります。

これにより、usernameフィールドにメールアドレスがセットされていても、正常にログイン処理が進むというわけです。

------------------------------------------------------------------------------------------------------
Djangoでユーザー認証を行う際、emailやusernameで認証するかどうかの設定は、主に以下の2つの場所で設定されています。

1. USERNAME_FIELD の設定 (ユーザーモデル)

Djangoのカスタムユーザーモデルを使う場合、USERNAME_FIELDというフィールドで、ユーザー認証に使用するフィールドを指定します。デフォルトのDjangoのUserモデルではusernameが使われますが、カスタムユーザーモデルでemailを使って認証したい場合は、次のように設定します。

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'  # 認証に使うフィールドをemailに変更
    REQUIRED_FIELDS = []  # 必須で入力させたいフィールドを指定

    objects = CustomUserManager()

このように、USERNAME_FIELD = 'email'と設定することで、Djangoの認証システムがユーザー名の代わりにメールアドレスを使ってユーザーを認証するようになります。

2. AUTHENTICATION_BACKENDS の設定 (バックエンド)

Djangoの認証バックエンドをカスタマイズすることもできます。デフォルトでは、usernameフィールドが認証に使用されますが、複数のフィールド（例: usernameやemail）を使って認証したい場合は、バックエンドをカスタマイズすることで可能になります。

例えば、次のように認証バックエンドを追加することで、usernameとemailのどちらでもログインできるように設定できます。

# settings.py

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # デフォルトのバックエンド
    'path.to.EmailOrUsernameBackend',  # カスタムバックエンド
]

そして、カスタム認証バックエンドを作成します。

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # usernameがメールアドレスの場合、メールでユーザーを取得
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            # usernameが通常のユーザー名の場合
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None

このバックエンドでは、usernameとしてメールアドレスか通常のユーザー名のどちらかが入力された場合、それぞれに対応してユーザー認証を行います。

まとめ

	•	USERNAME_FIELD: カスタムユーザーモデルでユーザー認証に使用するフィールド（例えば、email）を指定するために使用します。
	•	AUTHENTICATION_BACKENDS: Djangoで認証方法をカスタマイズしたい場合に使用し、複数のフィールド（usernameやemailなど）を使って認証を行う場合はカスタムバックエンドを設定します。

この2つを適切に設定することで、emailやusernameで認証できるようにすることが可能です。
