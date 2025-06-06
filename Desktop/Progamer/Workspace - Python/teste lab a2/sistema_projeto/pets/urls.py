from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pets/', views.listar_pets, name='listar_pets'),
    path('cadastrar/', views.cadastrar_pet, name='cadastrar_pet'),
    path('editar/<int:pet_id>/', views.editar_pet, name='editar_pet'),
    path('remover/<int:pet_id>/', views.remover_pet, name='remover_pet'),
]
