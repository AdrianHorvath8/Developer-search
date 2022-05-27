from django.forms import ModelForm
from .models import Skill
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .models import Profile, Message

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "email", "username", "password1", "password2"]


    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

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


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user"]


    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class":"input"})




class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ["name","description"]
        
    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class":"input"})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["name","email", "subject", "body"]
        
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class":"input"})