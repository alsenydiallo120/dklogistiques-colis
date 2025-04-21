from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import *

urlpatterns = [
	path('', login_required(index.as_view()),name='decaissements-index'),
	path('create/',login_required(create.as_view()),name='decaissements-create'),
	path('edit/<int:pk>/',login_required(edit.as_view()),name='decaissements-edit'),
	path('delete/<int:pk>/',login_required(delete.as_view()),name='decaissements-delete'),
    path("view_decaissements/",login_required(view_decaissements),name="view_decaissements"),
    path("encaissement_enattente/",login_required(encaissement_enattente.as_view()),name="encaissement_enattente"),
    path("encaissement_valide/",login_required(encaissement_valide.as_view()),name="encaissement_valide"),
    path('valide_encaissement/<int:pk>/',login_required(valide_encaissement.as_view()),name='valide_encaissement'),
]
