from os import stat_result
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.shortcuts import redirect
from django.utils.functional import lazy

def get_collaborators(project):
    return project.collaborators.objects.all()

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=2000, null=False)
    description = RichTextField(null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects', null=True)
    time = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=50, null=False)
    pro_id = models.CharField(max_length=4, null=False)

    def __str__(self):
        return f"{self.code}-{self.id} - {self.name}"

    def __repr__(self):
        return repr(f"{self.code}-{self.id} - {self.name}")


class Collaborator(models.Model):
    user = models.ForeignKey(User, related_name='in_projects', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name="collaborators", on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.project}"

class Work(models.Model):
    project = models.ForeignKey(Project, related_name="works", on_delete=models.CASCADE,null=True, blank=True)
    header = models.CharField(max_length=2000,null=True, blank=True)
    assigned_to = models.ForeignKey(User, related_name='works', on_delete=models.CASCADE, null=True)
    work = RichTextField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('Not Completed','Not Completed'),
        ('Completed','Completed'),
        ('Hidden','Hidden')
    ],null=True, blank=True)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self._meta.get_field('user').choices = lazy(get_collaborators(self.project), list)

    def __str__(self):
        return f"{self.project} {self.assigned_to}"

class File(models.Model):
    work = models.ForeignKey(Work, related_name='files', on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='file/')
    user = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.work} {self.file}"

