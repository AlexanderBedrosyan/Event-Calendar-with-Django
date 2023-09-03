from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'})) # this widget will change the structure in the web-page. The part with class:form-control, this is html which directly change the view
    first_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta: # this is using by convention of Django
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
