from django.urls import path
from .views import register,liste,edit,login_client
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views
from .views import *

urlpatterns = [
    path('register/',login_required(register.as_view()),name="accounts-register"),
    path('liste/',login_required(liste.as_view()),name="accounts-listes"),
    path('edit/<int:pk>/',login_required(edit.as_view()),name="accounts-edit"),
    path('connexion/',login_client,name="accounts-login"),
    path('reset_password/<int:pk>/',login_required(reset_password.as_view()),name="reset_password"),
    path('logout/', Logout.as_view(),name='logout-view'),
    # ------------------------------PASSWORD RESET--------------------------------
    path('password_reset/', views.PasswordResetView.as_view(template_name="registration/password_reset.html"),name="password_reset"),
    path('password_reset_done/', views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>', views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('password_reset_complete/', views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
]
