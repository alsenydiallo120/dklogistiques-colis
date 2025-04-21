from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import *

urlpatterns = [
	path('', login_required(index.as_view()),name='clients-index'),
	path('create_new/', login_required(create_new.as_view()),name='create_new'),
	path('send_colis/', login_required(send_colis.as_view()),name='send_colis'),
	path('add_new_destinataire/', login_required(add_new_destinataire.as_view()),name='add_new_destinataire'),
	path('add_new_destinataire_bateau/', login_required(add_new_destinataire_bateau.as_view()),name='add_new_destinataire_bateau'),
	path('create/',login_required(create.as_view()),name='clients-create'),
	path('edit/<int:pk>/',login_required(edit.as_view()),name='clients-edit'),
	path('edit_from_colis/<int:pk>/',login_required(edit_from_colis.as_view()),name='clients-edit_from_colis'),
	path('delete/<int:pk>/',login_required(delete.as_view()),name='clients-delete'),
]
