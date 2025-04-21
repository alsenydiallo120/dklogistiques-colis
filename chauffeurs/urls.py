from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import index,create,edit,delete

urlpatterns = [
	path('', login_required(index.as_view()),name='chauffeurs-index'),
	path('create/',login_required(create.as_view()),name='chauffeurs-create'),
	path('edit/<int:pk>/',login_required(edit.as_view()),name='chauffeurs-edit'),
	path('delete/<int:pk>/',login_required(delete.as_view()),name='chauffeurs-delete'),
]
