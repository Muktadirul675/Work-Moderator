from django import forms
from django.db.models import fields
from django.forms import models, widgets
from . import models

class AddProject(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = "__all__"
        exclude = ['time', 'pro_id', 'owner']
        labels = {
            'name': 'Project Name',
            'description': 'Project Description',
            'code': 'Project Code',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control',}),
            'description': forms.Textarea(attrs={'class':'form-control',}),
            'code': forms.TextInput(attrs={'class':'form-control',}),
        }

class AddWork(forms.ModelForm):
    class Meta:
        model = models.Work
        fields = ['header','work','status']
        labels = {
            'header': 'Work Header' ,
            'work': 'Work Description' ,
            'status': 'Work status' ,
            'user' : 'User: '
        }
        widgets = {
            'header': forms.TextInput(attrs={'class':'form-control',}),
            'work': forms.Textarea(attrs={'class':'form-control',}),
        }

class AttachFile(forms.ModelForm):
    class Meta:
        model = models.File
        fields = {'file_name','file',}
        labels = {
            'file_name':'File Name',
            'file': 'Project Attachment '          
        }
        widgets = {
            'file_name': forms.TextInput(attrs={'class':'form-control'}),
            'file' : forms.FileInput(attrs={'class':'form-control'})
        }
