from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.profile_index, name='index'),
    path('edit/', views.profile_edit, name='edit'),
    path('edit/skills/create/', views.skill_create, name='skill_create'),
    path('edit/skills/<int:skill_id>/delete/', views.skill_delete, name='skill_delete'),
    path('edit/experiences/create/', views.experience_create, name='experience_create'),
    path('edit/experiences/<int:exp_id>/delete/', views.experience_delete, name='experience_delete'),
    path('edit/projects/create/', views.project_create, name='project_create'),
    path('edit/projects/<int:project_id>/delete/', views.project_delete, name='project_delete'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
]
