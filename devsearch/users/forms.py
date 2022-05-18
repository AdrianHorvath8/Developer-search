from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "email", "username", "password1", "password2"]


    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__()

        self.fields["first_name"].widget.attrs.update(
            {"class":"input", "placeholder":"Add name"})
        
        self.fields["email"].widget.attrs.update(
            {"class":"input"})
        
        self.fields["username"].widget.attrs.update(
            {"class":"input"})
        
        self.fields["password1"].widget.attrs.update(
            {"class":"input"})

        self.fields["password2"].widget.attrs.update(
            {"class":"input"})