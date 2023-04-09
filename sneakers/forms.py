from django.forms import Form, CharField, PasswordInput
from captcha.fields import CaptchaField

class LoginForm(Form):
    username = CharField(max_length=100)
    password = CharField(widget=PasswordInput())
    captcha = CaptchaField()