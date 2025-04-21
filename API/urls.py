from .views import *
from django.urls import path


urlpatterns = [
    path('scanner/<int:pk>/', (scanner)),
    path('get_coli_info/<str:code>/', get_coli_info.as_view()),
    path('add_rendez_vous/', add_rendez_vous.as_view()),
    path('add_demande_devis/', add_demande_devis.as_view()),
    #----------------------------------------------
    path('liste_rendez_vous/', liste_rendez_vous.as_view()),
    path('list_demande_devis/', list_demande_devis.as_view()),
]