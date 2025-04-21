from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import *

urlpatterns = [
	path('', login_required(index.as_view()),name='depensevols-index'),
	path('create/',login_required(create.as_view()),name='depensevols-create'),
	path('edit/<int:pk>/',login_required(edit.as_view()),name='depensevols-edit'),
	path('delete/<int:pk>/',login_required(delete.as_view()),name='depensevols-delete'),
	path('add_depensevols/',login_required(add_depensevols),name='add_depensevols'),
]
