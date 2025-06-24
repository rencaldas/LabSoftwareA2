from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pets/', views.listar_pets, name='listar_pets'),
    path('cadastrar/', views.cadastrar_pet, name='cadastrar_pet'),
    path('gerenciar/', views.gerenciar_pets, name='gerenciar_pets'),
    path('editar/<int:pet_id>/', views.editar_pet, name='editar_pet'),
    path('remover/<int:pet_id>/', views.remover_pet, name='remover_pet'),
    path('pet/<int:pet_id>/', views.pet_detalhe, name='pet_detalhe'),  
    path('adotar/', views.listar_animais_disponiveis, name='listar_animais'),
    path('meus-dados/editar/', views.editar_dados, name='editar_dados'),
    path('meus-dados/', views.meus_dados, name='meus_dados'),
    path('meus-aumigos/', views.meus_aumigos, name='meus_aumigos'),
    path('adotar/<int:pet_id>/', views.adotar_pet, name='adotar_pet'),
    path('cancelar-adocao/<int:adocao_id>/', views.cancelar_adocao, name='cancelar_adocao'),
]
