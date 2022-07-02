from django.db import models
from django.contrib.auth.models import User
import uuid

    

class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
    primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=300, null= True, blank=True)
    short_info = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(blank=False, null=False, upload_to="profiles/", default="profiles/user-default.png")
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    social_stackoverflow = models.CharField(max_length=200, blank=True, null=True)
    
    
    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return str(self.username)


class Skill(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
    primary_key=True, editable=False)
    skill = models.ForeignKey(Profile,on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str(self.name)


class Message(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
    primary_key=True, editable=False)
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    class Meta:
        ordering = ['is_read', '-created']

