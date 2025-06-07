from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages
from .models import Pet, Adocao
from .forms import PetForm, AdocaoForm, CustomUserChangeForm

def index(request):
    pets = Pet.objects.all()
    return render(request, 'pets/index.html', {'pets': pets})

def listar_pets(request):
    pets = Pet.objects.all()
    return render(request, 'pets/listar_pets.html', {'pets': pets})

def cadastrar_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_pets')
    else:
        form = PetForm()
    return render(request, 'pets/cadastrar_pet.html', {'form': form})

def editar_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_pets')  # Alterado aqui para redirecionar para a página de gerenciamento
    else:
        form = PetForm(instance=pet)

    return render(request, 'pets/editar_pet.html', {'form': form, 'pet': pet})

def remover_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        pet.delete()
        return redirect('listar_pets')
    context = {'pet': pet}
    return render(request, 'pets/remover_pet.html', context)

def pet_detalhe(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'pets/pet_detalhe.html', {'pet': pet})

def gerenciar_pets(request):
    pets = Pet.objects.all()

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_pets')
    else:
        form = PetForm()

    context = {
        'pets': pets,
        'form': form,
    }
    return render(request, 'pets/gerenciar_pets.html', context)

def listar_animais_disponiveis(request):
    pets = Pet.objects.all()
    return render(request, 'pets/listar_animais.html', {'pets': pets})

@login_required
def adotar_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        form = AdocaoForm(request.POST, request.FILES)
        if form.is_valid():
            adocao = form.save(commit=False)
            adocao.pet = pet
            adocao.usuario = request.user
            adocao.email_adotante = request.user.email
            adocao.save()

            if hasattr(pet, 'disponivel'):
                pet.disponivel = False
                pet.save()

            return render(request, 'pets/adocao_sucesso.html', {'pet': pet})
        else:
            return render(request, 'pets/adotar_pet.html', {
                'form': form,
                'pet': pet,
                'form_errors': form.errors,
            })
    else:
        form = AdocaoForm()

    return render(request, 'pets/adotar_pet.html', {'form': form, 'pet': pet})

@login_required
def meus_dados(request):
    return render(request, 'pets/meus_dados.html')

@login_required
def meus_aumigos(request):
    aumigos = Adocao.objects.filter(email_adotante=request.user.email).select_related('pet')
    context = {
        'aumigos': aumigos,
    }
    return render(request, 'pets/meus_aumigos.html', context)

@login_required
def editar_dados(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seus dados foram atualizados com sucesso.')
            return redirect('meus_dados')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'pets/editar_dados.html', {'form': form})

@login_required
def cancelar_adocao(request, adocao_id):
    adocao = get_object_or_404(Adocao, id=adocao_id)

    # Verifica se o usuário atual é o dono da adoção
    if adocao.email_adotante != request.user.email:
        messages.error(request, 'Você não tem permissão para cancelar esta adoção.')
        return redirect('meus_aumigos')

    if request.method == 'POST':
        adocao.delete()
        messages.success(request, 'Adoção cancelada com sucesso.')
        return redirect('meus_aumigos')

    # Se quiser, pode criar um template para confirmar o cancelamento
    return render(request, 'pets/cancelar_adocao_confirmar.html', {'adocao': adocao})