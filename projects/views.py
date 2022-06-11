from django.shortcuts import render, redirect
from . models import Project, Tag
from . forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def projects (request):
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    tag = Tag.objects.filter(name__icontains = search_query)
    
    projects = Project.objects.distinct().filter(
    Q(title__icontains = search_query)|
    Q(description__icontains = search_query) |
    Q(tags__in = tag) |
    Q(owner__name__icontains = search_query) 
       )

    

    context = {"projects":projects, "search_query":search_query,}
    return render(request, "projects/projects.html", context)


def project(request, pk):
    project = Project.objects.get(id=pk)

    form = ReviewForm()
   
    try:
        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.owner = request.user.profile
                review.project = project
                review.save()
                
                project.get_vote_count


                messages.success(request, "Your review was created")
                return redirect("project", pk=project.id)
    except:
        messages.error(request, "You already review this project")




    context = {"project":project, "form":form}
    return render(request, "projects/project.html", context)


@login_required(login_url="login")
def create_project(request):
    form = ProjectForm()
    if request.method == "POST":
        newtags = request.POST.get("newtags").replace(","," ").split()
        form = ProjectForm(request.POST, request.FILES)
        
        if form.is_valid():
            project = form.save(commit = False)
            project.owner = request.user.profile
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(
                    name = tag
                )
                project.tags.add(tag)
            
            
            return redirect("account", pk = request.user.profile.id)

    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def update_project(request,pk):
    page = "update"
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    tags = project.tags.all()
    form = ProjectForm(instance=project)
    if request.method == "POST":
        newtags = request.POST.get("newtags").replace(","," ").split()
        
        form = ProjectForm(request.POST, request.FILES , instance=project)

        if form.is_valid():
            projects= form.save(commit=False)
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(
                    name = tag
                )
                projects.tags.add(tag)
            projects.save()
            
            return redirect("account", pk = request.user.profile.id)

    context = {"form": form,"tags":tags,"page":page}
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


