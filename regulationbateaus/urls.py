from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import *

urlpatterns = [
	path('', login_required(index.as_view()),name='regulationbateaus-index'),
	path('create/',login_required(create.as_view()),name='regulationbateaus-create'),
	path('edit/<int:pk>/',login_required(edit.as_view()),name='regulationbateaus-edit'),
	path('delete/<int:pk>/',login_required(delete.as_view()),name='regulationbateaus-delete'),
    path('regulationbateaus_print/<int:pk>/',login_required(regulationbateaus_print),name='regulationbateaus_print'),
]
