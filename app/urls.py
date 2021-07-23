from os import name
import django
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'app'

urlpatterns = [
    path("",  views.home, name="home"),
    path('create_project/', views.create_project, name="create_project"),
    path("project/<int:id>/", views.project, name="project"),
    path('login/', views.user_login ,name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("sign_up/", views.signup, name="sign_up"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path('join_project/',views.join_project, name="join_project"),
    path('project/<int:project_id>/add_work/', views.add_work, name="add_work"),
    path('project/<int:project_id>/work/<int:work_id>/assign_work/<int:user_id>/', views.assign_work, name="assign_work"),
    path('project/<int:project_id>/work/<int:work_id>/', views.work,name='work'),
    path('project/<int:project_id>/leave/', views.leave, name='leave'),
    path('project/<int:project_id>/user/<int:user_id>/kick/',views.kick, name="kick"),
] 


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)