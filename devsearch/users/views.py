from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from projects.views import project, projects
from .models import Profile
from .models import Skill
from .forms import CustomUserCreationForm, SkillForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


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
            return redirect("edit_account")

        else:
            messages.error(request, "An error during registration")

    context = {"page" : page,"form":form}
    return render(request, "users/login_register.html", context)


def profiles (request):
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    skill = Skill.objects.filter(name__icontains=search_query)

    profiles= Profile.objects.distinct().filter(
    Q(name__icontains = search_query) |
    Q(short_info__icontains = search_query)| 
    Q(skill__in = skill)
     )

    page = request.GET.get("page")
    paginator= Paginator(profiles, 6)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    left_index = (int(page) - 4)

    if left_index <1:
        left_index = 1

    right_index = (int(page) + 5)

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages+1

    custom_range= range(left_index,right_index)
    


    context = {"profiles":profiles, "search_query":search_query,"custom_range":custom_range}
    return render(request, "users/profiles.html", context)


def profile (request, pk):
    profile= Profile.objects.get(id=pk)
    skills_with_description = profile.skill_set.exclude(description__exact="")
    skills_no_description = profile.skill_set.filter(description="")

    context = {"profile":profile, "skills_no_description":skills_no_description, "skills_with_description":skills_with_description}
    return render(request, "users/user_profile.html", context)


@login_required(login_url="login")
def user_account (request, pk):
    account= Profile.objects.get(id=pk)
   
    if account.id == request.user.profile.id:
        pass
    else:
        
        return redirect("account", pk=request.user.profile.id)
    
    context = {"account":account,}
    return render(request, "users/account.html", context)


@login_required(login_url="login")
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES ,instance=profile)

        if form.is_valid():
            form.save()

            return redirect ("account", pk = request.user.profile.id)

    context = {"form": form}
    return render(request, "users/profile_form.html", context)


@login_required(login_url="login")
def skill_edit(request, pk):
    skill = Skill.objects.get(id=pk)
    account = skill.skill.id
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)

        if form.is_valid():
            form.save()
            messages.success(request, "Skill was updated successfuly")
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
            messages.success(request, "Skill was added successfuly")
            return redirect("account", pk=accound_id)
            

    context = {"form":form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def skill_delete(request, pk):
    obj = Skill.objects.get(id=pk)
    accound_id = request.user.profile.id
    obj.delete()
    messages.success(request, "Skill was delete successfuly")
    return redirect("account", pk=accound_id)


