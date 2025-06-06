from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),

    #ROTA PARA ADMINISTRADOR
    path('gerenciar/', views.gerenciar_pets_view, name='gerenciar_pets'),
]
