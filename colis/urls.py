from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import *

urlpatterns = [
    path('', login_required(index.as_view()),name='colis-index'),
	path('bateau/', login_required(bateau.as_view()),name='colis-bateau'),
	path('etat_colis/', login_required(etat_colis.as_view()),name='etat_colis'),
	path('create/',login_required(create.as_view()),name='colis-create'),
	path('create_bateau/',login_required(create_bateau.as_view()),name='colis-create_bateau'),
	path('edit/<int:pk>/',login_required(edit.as_view()),name='colis-edit'),
	path('edit_colis_bateau/<int:pk>/',login_required(edit_colis_bateau.as_view()),name='colis-edit_colis_bateau'),
	path('delete/<int:pk>/',login_required(delete.as_view()),name='colis-delete'),
	path('delete_colis_bateau/<int:pk>/',login_required(delete_colis_bateau.as_view()),name='colis-delete_colis_bateau'),
	path('detail/<int:pk>/',login_required(detail.as_view()),name='colis-detail'),
	path('print/<int:pk>/',login_required(print_facture),name='colis-print'),
	path('print_facture_bateau/<int:pk>/',login_required(print_facture_bateau),name='print_facture_bateau'),
	path('find_colis/',login_required(find_colis),name='find_colis'),
	path('mon_rapport/',login_required(mon_rapport),name='mon_rapport'),
	path('print_rapport/',login_required(print_rapport),name='print_rapport'),
	path('get_destinataire/',login_required(get_destinataire),name='get_destinataire'),
	path('nouveau_client/',login_required(nouveau_client),name='nouveau_client'),
	path('colis_add_item/',login_required(colis_add_item),name='colis_add_item'),
	path('colis_delete_item/<int:pk>/',login_required(colis_delete_item),name='colis_delete_item'),
	path('valide_colis_bateau/<int:pk>/',login_required(valide_colis_bateau),name='valide_colis_bateau'),
	path('remove_validate_colis_bateau/<int:pk>/',login_required(remove_validate_colis_bateau),name='remove_validate_colis_bateau'),
	path('print_list_colis_conteneur/',login_required(print_list_colis_conteneur),name='print_list_colis_conteneur'),
	path('filter_colis/',login_required(filter_colis),name='filter_colis'),
	path('get_clients/',login_required(get_clients),name='get_clients'),
	path('get_codes_vol/',login_required(get_codes_vol),name='get_codes_vol'),
	path('get_colis_info/',login_required(get_colis_info),name='get_colis_info'),
	path('get_colis_reglement/',login_required(get_colis_reglement),name='get_colis_reglement'),
]
