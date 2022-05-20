from django.shortcuts import render, redirect
from . models import Project, Tag, Review
from . forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def projects (request):
    projects = Project.objects.all()
    context = {"projects":projects}
    return render(request, "projects/projects.html", context)

def project(request, pk):
    project = Project.objects.get(id=pk)
    context = {"project":project}
    return render(request, "projects/project.html", context)


@login_required(login_url="login")
def create_project(request):
    form = ProjectForm()
    if request.method == "POST":

        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit = False)
            user.owner = request.user.profile
            user.save()
            
            return redirect("account", pk = request.user.profile.id)

    context = {"form": form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def update_project(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":

        form = ProjectForm(request.POST, request.FILES , instance=project)

        if form.is_valid():
            form.save()
            
            return redirect("account", pk = request.user.profile.id)

    context = {"form": form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def delete_project(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    

    if request.method == "POST":

        project.delete()
        messages.success(request, "Project was delete successfuly")
        return redirect("account", pk = request.user.profile.id)
    context = {"obj": project}
    return render(request, "projects/delete_template.html", context)