from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from . models import CustomUser


class CreateUserForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'is_writer']


class UpdateUserForm(ModelForm):

    password = None

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']
        exclude = ['password1', 'password2']
