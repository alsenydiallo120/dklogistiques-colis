
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('', auth_views.LoginView.as_view()),
    path('login/', auth_views.LoginView.as_view()),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/profile/', home,name='home'),
    path('entreprise/', include('entreprise.urls')),
    path('typecomptes/',include('typecomptes.urls')),
    path('agences/',include('agences.urls')),
    path('pays/',include('pays.urls')),
    path('transporteurs/',include('transporteurs.urls')),
    path('tauxs/',include('tauxs.urls')),
    path('expeditaires/',include('expeditaires.urls')),
    path('destinataires/',include('destinataires.urls')),
    path('colis/',include('colis.urls')),
    path('lots/',include('lots.urls')),
    path('embarquements/',include('embarquements.urls')),
    path('depenses/',include('depenses.urls')),
    path('API/',include('API.urls')),
    path('depots/',include('depots.urls')),
    path('reglements/',include('reglements.urls')),
    path('clients/',include('clients.urls')),
    path('conteneurs/',include('conteneurs.urls')),
    path('annees/',include('annees.urls')),
    path('regulations/',include('regulations.urls')),
    path('decaissements/',include('decaissements.urls')),
    path('depensevols/',include('depensevols.urls')),
    path('rendezvous/',include('rendezvous.urls')),
    path('regulationbateaus/',include('regulationbateaus.urls')),
    path('clientsrendezvous/',include('clientsrendezvous.urls')),
    path('chauffeurs/',include('chauffeurs.urls')),
    path('rapports/',login_required(rapports.as_view()),name='rapports'),
    path('rapport_jour/',login_required(rapport_jour.as_view()),name='rapport_jour'),
    path('rapport_jour_paris/',login_required(rapport_jour_paris.as_view()),name='rapport_jour_paris'),
    path('dashboard_admin/',login_required(dashboard_admin),name='dashboard_admin'),
    path('__debug__/', include('debug_toolbar.urls')),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'accounts.views.page_not_found'

