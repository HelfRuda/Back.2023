from django.forms import (
    modelform_factory,
    ModelForm,
)

from .models import User

class UserForm(ModelForm):

    class Meta:
        model = User
        fields = '__all__'