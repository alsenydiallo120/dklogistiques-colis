from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import index,create,edit,delete,detail

urlpatterns = [
	path('', login_required(index.as_view()),name='lots-index'),
	path('create/',login_required(create.as_view()),name='lots-create'),
	# path('add_lot/',login_required(add_lot),name='add_lot'),
	path('edit/<int:pk>/',login_required(edit.as_view()),name='lots-edit'),
	path('lots-detail/<int:pk>/',login_required(detail.as_view()),name='lots-detail'),
	path('delete/<int:pk>/',login_required(delete.as_view()),name='lots-delete'),
]
