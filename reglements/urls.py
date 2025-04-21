from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import *

urlpatterns = [
	path('', login_required(index.as_view()),name='reglements-index'),
	path('reglements_add/',login_required(reglements_add),name='reglements_add'),
	path('create/',login_required(create.as_view()),name='reglements-create'),
	path('create_guinee/',login_required(create_guinee.as_view()),name='reglements-create_guinee'),
	path('create_bateau/',login_required(create_bateau.as_view()),name='reglements-create-bateau'),
	path('edit/<int:pk>/',login_required(edit.as_view()),name='reglements-edit'),
	path('delete/<int:pk>/',login_required(delete.as_view()),name='reglements-delete'),
	path('get_reste/',login_required(get_reste),name='get_reste'),
	path('get_colis_vol/',login_required(get_colis_vol),name='get_colis_vol'),
	path('reglements_print/<int:pk>/',login_required(reglements_print),name='reglements_print'),
    path('update_colis_vol/',login_required(update_colis_vol),name='update_colis_vol'),
]
