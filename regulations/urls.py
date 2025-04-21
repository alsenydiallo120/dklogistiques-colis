from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import *

urlpatterns = [
	path('', login_required(index.as_view()),name='regulations-index'),
	path('create/',login_required(create.as_view()),name='regulations-create'),
	path('edit/<int:pk>/',login_required(edit.as_view()),name='regulations-edit'),
	path('delete/<int:pk>/',login_required(delete.as_view()),name='regulations-delete'),
    path('regulations_print/<int:pk>/',login_required(regulations_print),name='regulations_print'),
    path('get_info_colis_regulation/',login_required(get_info_colis_regulation),name='get_info_colis_regulation'),
    path('get_info_colis_regulation_bateau/',login_required(get_info_colis_regulation_bateau),name='get_info_colis_regulation_bateau'),
    path('get_colis_regulations/',login_required(get_colis_regulations),name='get_colis_regulations'),
    path('get_colis_regulation_bateau/',login_required(get_colis_regulation_bateau),name='get_colis_regulation_bateau'),
]
