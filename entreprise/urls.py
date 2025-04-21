from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import index,create,edit

urlpatterns = [
    path('', login_required(index.as_view()),name='entreprise-index'),
    path('create/',login_required(create.as_view()),name='entreprise-create'),
    path('edit/<int:pk>/',login_required(edit.as_view()),name='entreprise-edit'),
]
