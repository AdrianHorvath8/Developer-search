
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import Profile
from django.contrib.auth.models import User
from .models import Skill
from .forms import CustomUserCreationForm, SkillForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def login_user(request):

    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        

        user = authenticate(request, username=username, password=password)


        if user != None:
            login(request, user)
            return redirect("profiles")
        else:
            messages.error(request, "Username or password is incorect")
    context = {}
    return render(request, "users/login_register.html", context)


def logout_user(request):
    logout(request)
    messages.info(request, "User was logout")
    return redirect("profiles")


def register_user(request):
    page= "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "User successfuly created")
            login(request, user)
            return redirect("profiles")

        else:
            messages.error(request, "An error during registration")

    context = {"page" : page,"form":form}
    return render(request, "users/login_register.html", context)

def profiles (request):
    profiles= Profile.objects.all()
    context = {"profiles":profiles}
    return render(request, "users/profiles.html", context)

def profile (request, pk):
    profile= Profile.objects.get(id=pk)
    skills_with_description = profile.skill_set.exclude(description__exact="")
    skills_no_description = profile.skill_set.filter(description="")
    context = {"profile":profile, "skills_no_description":skills_no_description, "skills_with_description":skills_with_description}
    return render(request, "users/user_profile.html", context)

def user_account (request, pk):
    account= Profile.objects.get(id=pk)
    # nefunguje
    if account.id == request.user.profile.id:
        pass
    else:
        HttpResponse("You are not allowed here")
        return redirect("account", pk=request.user.profile.id)
    
    context = {"account":account,}
    return render(request, "users/account.html", context)
    
@login_required(login_url="login")
def skill_edit(request, pk):
    skill = Skill.objects.get(id=pk)
    account = skill.skill.id
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)

        if form.is_valid():
            form.save()
            return redirect("account", pk=account)

    context = {"form":form}
    return render(request, "users/skill_form.html", context)

@login_required(login_url="login")
def skill_create(request):
    
    form = SkillForm()
    accound_id = request.user.profile.id
    

    if request.method == "POST":
        form = SkillForm(request.POST)

        if form.is_valid():
            user = form.save(commit = False)
            user.skill = request.user.profile
            user.save()
            return redirect("account", pk=accound_id)
            

    context = {"form":form}
    return render(request, "users/skill_form.html", context)

@login_required(login_url="login")
def skill_delete(request, pk):
    obj = Skill.objects.get(id=pk)
    accound_id = request.user.profile.id
    obj.delete()
    return redirect("account", pk=accound_id)
