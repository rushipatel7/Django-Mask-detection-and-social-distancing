from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        for k, v in self.fields.items():
            v.widget.attrs['placeholder'] = k.replace('_', ' ').capitalize()
            if k == 'password1':
                v.widget.attrs['placeholder'] = 'Password'
            if k == 'password2':
                v.widget.attrs['placeholder'] = 'Confirm Password'
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")
