from django.shortcuts import render, redirect, get_object_or_404
from .models import Pet
from .forms import PetForm

def listar_pets(request):
    pets = Pet.objects.all()
    return render(request, 'listar_pets.html', {'pets': pets})

def cadastrar_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_pets')
    else:
        form = PetForm()
    return render(request, 'cadastrar_pet.html', {'form': form})

def editar_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        form = PetForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('listar_pets')
    else:
        form = PetForm(instance=pet)
    return render(request, 'editar_pet.html', {'form': form})

def remover_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        pet.delete()
        return redirect('listar_pets')
    return render(request, 'remover_pet.html', {'pet': pet})
