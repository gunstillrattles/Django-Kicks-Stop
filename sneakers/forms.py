from django.forms import Form, CharField, PasswordInput
from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(Form):
    username = CharField(max_length=100)
    password = CharField(widget=PasswordInput())
    captcha = CaptchaField()


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
