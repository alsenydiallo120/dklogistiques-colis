from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import *

urlpatterns = [
	path('', login_required(index.as_view()),name='conteneurs-index'),
	path('create/',login_required(create.as_view()),name='conteneurs-create'),
	path('edit/<int:pk>/',login_required(edit.as_view()),name='conteneurs-edit'),
	path('delete/<int:pk>/',login_required(delete.as_view()),name='conteneurs-delete'),
	path('cloturer/<int:pk>/',login_required(cloturer.as_view()),name='conteneurs-cloturer'),
]
