from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pets/', views.listar_pets, name='listar_pets'),  # opcional: pode comentar/remover
    path('cadastrar/', views.cadastrar_pet, name='cadastrar_pet'),  # opcional: pode comentar/remover
    path('gerenciar/', views.gerenciar_pets, name='gerenciar_pets'),  # nova rota gerenciar pets
    path('editar/<int:pet_id>/', views.editar_pet, name='editar_pet'),
    path('remover/<int:pet_id>/', views.remover_pet, name='remover_pet'),
    path('pet/<int:pet_id>/', views.pet_detalhe, name='pet_detalhe'),  
]
