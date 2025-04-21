from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import *

urlpatterns = [
	path('', login_required(index.as_view()),name='depenses-index'),
	path('create/',login_required(create.as_view()),name='depenses-create'),
	path('edit/<int:pk>/',login_required(edit.as_view()),name='depenses-edit'),
	path('delete/<int:pk>/',login_required(delete.as_view()),name='depenses-delete'),
	path('add_depenses/',login_required(add_depenses),name='add_depenses'),
]
