from django.contrib.messages.api import MessageFailure
from django.db.models.query import FlatValuesListIterable, RawQuerySet
from django.db.models.query_utils import refs_expression
from django.forms.models import ModelMultipleChoiceField, model_to_dict
from django.shortcuts import render, redirect, resolve_url
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from . import models
from . import forms
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
import random

# Create your views here.

def generate_id():
    ids = []
    for i in models.Project.objects.all():
        ids.append(i.pro_id)
    id = random.randint(1000,9999)
    while id in ids:
        id = random.randint(1000,9999)
    print(id)
    return str(id)

def is_a_collaborator(project, user):
    for i in project.collaborators.all():
        if i.user == user:
            return True
    return False

#########################

def home(request):
    if request.user.is_authenticated:
        return redirect(f"profile/{request.user.username}")
    return render(request, 'home.html')

def homepage(request):
    return render(request, 'home.html')

@login_required(login_url="/login/")
def create_project(request):
    form = forms.AddProject()
    if request.method == "POST":
        form = forms.AddProject(request.POST)
        if form.is_valid():
            id = generate_id()
            form.save()
            latest_project = models.Project.objects.last()
            latest_project.pro_id = id
            latest_project.owner = request.user
            latest_project.save()
            messages.success(request, f'{latest_project.name} project created. The project code is {latest_project.code}-{id}. Use it to invite members.')
            clb = models.Collaborator()
            clb.user = request.user
            clb.project = latest_project
            clb.save()
            return redirect(f"/project/{id}/")
    cont = {'form':form}

    return render(request, 'create_project.html', cont)

@login_required(login_url="/login/")
def join_project(request):
    if request.user.is_authenticated:
        project = None
        id = None
        code = request.POST['code']
        for i in models.Project.objects.all():
            if f"{i.code}-{i.pro_id}" == code:
                project = i
                id = i.pro_id
                break
        else:
            return redirect("app:home")
        for i in project.collaborators.all():
            if i.user == request.user:
                return redirect(f"/project/{id}/")

        new_clb = models.Collaborator()
        new_clb.user = request.user
        new_clb.project = project
        new_clb.save()

        return redirect(f"/project/{id}/")
    else:
        return redirect("app:login")

@login_required(login_url="/login/")
def project(request, id):
    project = models.Project.objects.get(pro_id=id)
    if is_a_collaborator(project, request.user):
        works = list(reversed(project.works.all()))
        add_work_form = forms.AddWork()
        users = project.collaborators.all()
        cont = {'p':project,'works':works, 'add_work_form':add_work_form,'users':users}

        return render(request, 'project.html', cont)
    else:
        return redirect("app:home")

@login_required(login_url="/login/")
def add_work(request,project_id):
    project = models.Project.objects.get(pro_id=project_id)
    if project.owner == request.user:
        form = forms.AddWork()
        cont = {'project':project, 'form':form}
        if request.method == "POST":
            form = forms.AddWork(request.POST)
            if form.is_valid():
                form.save()
                last_work = models.Work.objects.last()
                last_work.project = project
                last_work.save()
                return redirect(f"/project/{project_id}/")
        return render(request, 'add_work.html',cont)
    else:
        return redirect("tmc:home")

def make_id(num):
    trailing = ""
    for i in range(4-len(num)):
        trailing += "0"

    return f"user-{trailing}{num}"

def user_login(request):
    if request.user.is_authenticated:
        return redirect("app:home")
    else:

        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password'] 

            user = authenticate(username=make_id(username),password=password)

            if user is not None:
                login(request,user)
                messages.info(request, 'Logged in successfully.')
            else:
                messages.error(request, 'Sorry, the user id or the password is incorrect!')
                return redirect("app:login")

            return redirect(f'/profile/{user.username}')
        
        return render(request,'login.html')


def get_user_id():
    count = 0
    for i in User.objects.all():
        count += 1
    count += 1
    str_count = str(count)
    trailing = ""
    for i in range(4-len(str_count)):
        trailing += "0"

    return trailing + str_count


def signup(request):
    if request.user.is_authenticated:
        return redirect("app:home")
    
    if request.method == "POST":
        id = get_user_id()
        name = f"user-{id}"
        email = request.POST['email']
        pswd = request.POST['password']
        f_name = request.POST["first_name"]
        l_name = request.POST['last_name']

        new_user = User.objects.create_user(
            name, email, pswd
        )
        new_user.first_name = f_name
        new_user.last_name = l_name
        new_user.save()

        login(request, new_user)

        messages.info(request, f"Successfully registered. Your user id is {id}" )

        return redirect(f"/profile/{name}/")
            
    return render(request, 'sign_up.html')

@login_required(login_url="/login/")      
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("app:home")

@login_required(login_url="/login/")
def profile(request, username):
    user = User.objects.get(username=username)
    if username == request.user.username:
        projects_own = []
        projects_in = []
        for i in user.projects.all():
            projects_own.append(i)
        for i in user.in_projects.all():
            projects_in.append(i)

        cont = {'user':user,'projects_own':projects_own,'projects_own_count':len(projects_own), 'projects_in':projects_in,'projects_in_count':len(projects_in)}

        return render(request, 'profile.html', cont)
    else:
        return redirect("app:home")

@login_required(login_url="/login/")
def work(request,project_id,work_id):
    project = models.Project.objects.get(pro_id=project_id)
    if is_a_collaborator(project, request.user):
        work = models.Work.objects.get(id=work_id)
        form = forms.AttachFile()
        cont = {'project':project,'project_id':project_id ,'work':work, 'form':form,}

        if request.method == "POST":
            form = forms.AttachFile(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                last_file = models.File.objects.last()
                last_file.work = work
                last_file.user = request.user
                work.status = "Completed"
                work.save()
                last_file.save()
            else:
                print("NV")

        return render(request, 'work.html', cont)
    else:
        return redirect("tmc:home")

def change_work_status(request,project_id, work_id):
    work = models.Work.objects.get(pk=work_id)
    if request.method == 'POST':
        status = request.POST['status']
        work.status = status
        work.save()
    return redirect(f"/project/{project_id}/work/{work_id}/")

@login_required(login_url="/login/")
def assign_work(request,project_id ,work_id, user_id):
    project = models.Project.objects.get(pro_id=project_id)
    if request.user == project.owner:
        work = models.Work.objects.get(pk=work_id)
        user = models.Collaborator.objects.get(pk=user_id)
        work.assigned_to = user.user
        work.save()
        
        return redirect(f"/project/{project_id}/")
    else:
        return redirect("app:home")

# def edit_work(request,project_id,work_id):
    project = models.Project.objects.get(pro_id=project_id)
    work = models.Work.objects.get(pj=work_id)

    cont = {'project':project, 'work':work}

    return render(request, 'edit_work.html', cont)

@login_required(login_url="/login/")
def leave(request,project_id):
    project = models.Project.objects.get(pro_id=project_id)
    if is_a_collaborator(project, request.user):
        clb = project.collaborators.get(user=request.user)
        clb.delete()
    else:
        return redirect("app:home")

    return redirect("app:home")

@login_required(login_url="/login/")
def kick(request,project_id,user_id):
    project = models.Project.objects.get(pro_id=project_id)
    if is_a_collaborator(project, request.user):
        collaborator = project.collaborators.get(pk=user_id)
        collaborator.delete()
    else:
        return redirect("app:home")

    return redirect(f"/project/{project_id}/")

def delete_work(request,project_id,work_id ):
    work = models.Work.objects.get(pk=work_id)
    work.delete()

    return redirect(f"/project/{project_id}/")
