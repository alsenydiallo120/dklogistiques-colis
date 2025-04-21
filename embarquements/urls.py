from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import *

urlpatterns = [
	path('', login_required(index.as_view()),name='embarquements-index'),
	path('create/',login_required(create.as_view()),name='embarquements-create'),
	path('edit/<int:pk>/',login_required(edit.as_view()),name='embarquements-edit'),
	path('delete/<int:pk>/',login_required(delete.as_view()),name='embarquements-delete'),
	path('detail_embarquement/<int:pk>/',login_required(detail_embarquement.as_view()),name='detail_embarquement'),
]
