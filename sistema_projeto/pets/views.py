from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages
from .models import Pet, Adocao, Perfil
from .forms import PetForm, AdocaoForm, UsuarioForm, PerfilForm, CustomUserChangeForm

def index(request):
    pets = Pet.objects.filter(disponivel=True)  # ← CERTO, só pets disponíveis
    return render(request, 'pets/index.html', {'pets': pets})

def listar_pets(request):
    pets = Pet.objects.filter(disponivel=True)
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

def adotar_pet(request, pet_id):
    pet = get_object_or_404(Pet, pk=pet_id)

    if request.method == 'POST':
        form = AdocaoForm(request.POST, request.FILES)
        if form.is_valid():
            adocao = form.save(commit=False)
            adocao.pet = pet

            if request.user.is_authenticated:
                adocao.email_adotante = request.user.email

            adocao.save()

            # Marca pet como indisponível
            pet.disponivel = False
            pet.save()

            return render(request, 'pets/adotar_pet.html', {
                'pet': pet,
                'form': AdocaoForm(),
                'msg_sucesso': 'Adoção confirmada com sucesso! Seus dados foram salvos.'
            })
    else:
        form = AdocaoForm()

    return render(request, 'pets/adotar_pet.html', {'pet': pet, 'form': form})

@login_required
def meus_dados(request):
    user = request.user
    perfil = None
    adotacao = None

    try:
        perfil = Perfil.objects.get(user=user)
    except Perfil.DoesNotExist:
        perfil = None

    # Ajuste o filtro para achar a adoção do usuário, baseado no que fizer sentido no seu modelo
    # Se tiver FK para user, use filtro direto, senão use cpf do perfil
    if perfil:
        adotacao = Adocao.objects.filter(cpf_adotante=perfil.cpf).first()

    return render(request, 'pets/meus_dados.html', {
        'user': user,
        'perfil': perfil,
        'adotacao': adotacao,
    })

    # Buscar a adoção mais recente do usuário (filtrando pelo email)
    adotacao = Adocao.objects.filter(email_adotante=request.user.email).order_by('-data_adocao').first()

    context = {
        'user': request.user,
        'adotacao': adotacao,
    }
    return render(request, 'pets/meus_dados.html', context)

@login_required
def meus_aumigos(request):
    aumigos = Adocao.objects.filter(email_adotante=request.user.email).select_related('pet')
    context = {
        'aumigos': aumigos,
    }
    return render(request, 'pets/meus_aumigos.html', context)

@login_required
def editar_dados(request):
    user = request.user
    perfil, created = Perfil.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UsuarioForm(request.POST, instance=user)
        perfil_form = PerfilForm(request.POST, instance=perfil)

        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, "Dados atualizados com sucesso!")
            return redirect('meus_dados')
    else:
        user_form = UsuarioForm(instance=user)
        perfil_form = PerfilForm(instance=perfil)

    return render(request, 'pets/editar_dados.html', {
        'user_form': user_form,
        'perfil_form': perfil_form,
    })

@login_required
def cancelar_adocao(request, adocao_id):
    adocao = get_object_or_404(Adocao, id=adocao_id)

    # Verifica se o usuário atual é o dono da adoção
    if adocao.email_adotante != request.user.email:
        messages.error(request, 'Você não tem permissão para cancelar esta adoção.')
        return redirect('meus_aumigos')

    if request.method == 'POST':
        # Libera o pet para adoção novamente
        pet = adocao.pet
        pet.disponivel = True
        pet.save()

        # Exclui a adoção
        adocao.delete()

        messages.success(request, 'Adoção cancelada com sucesso.')
        return redirect('meus_aumigos')

    return render(request, 'pets/cancelar_adocao_confirmar.html', {'adocao': adocao})