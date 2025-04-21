from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import *

urlpatterns = [
	path('', login_required(index.as_view()),name='rendezvous-index'),
	path('create/',login_required(create.as_view()),name='rendezvous-create'),
	path('edit/<int:pk>/',login_required(edit.as_view()),name='rendezvous-edit'),
	path('delete/<int:pk>/',login_required(delete.as_view()),name='rendezvous-delete'),
    path('print_rendez_vous_jour/', login_required(print_rendez_vous_jour),name='print_rendez_vous_jour'),
    path('rendezvous_du_jour/', login_required(rendezvous_du_jour.as_view()),name='rendezvous_du_jour'),
]
