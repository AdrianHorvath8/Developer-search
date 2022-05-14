
from django.shortcuts import render
from .models import Profile


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