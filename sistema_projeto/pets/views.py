from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pet, Adocao, Perfil
from .forms import PetForm, AdocaoForm, UsuarioForm, PerfilForm

def index(request):
    """
    Página inicial: lista pets disponíveis para adoção.
    """
    pets = Pet.objects.filter(disponivel=True)
    return render(request, 'pets/index.html', {'pets': pets})

def listar_pets(request):
    """
    Lista pets disponíveis (mesma lógica de index, mas em outra URL/rota).
    """
    pets = Pet.objects.filter(disponivel=True)
    return render(request, 'pets/listar_pets.html', {'pets': pets})

def cadastrar_pet(request):
    """
    Cria novo Pet. Se for POST com dados válidos, salva e redireciona para listar_pets.
    """
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_pets')
    else:
        form = PetForm()
    return render(request, 'pets/cadastrar_pet.html', {'form': form})

def editar_pet(request, pet_id):
    """
    Edita Pet existente. Se POST válido, salva e redireciona para gerenciar_pets.
    """
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_pets')
    else:
        form = PetForm(instance=pet)
    return render(request, 'pets/editar_pet.html', {'form': form, 'pet': pet})

def remover_pet(request, pet_id):
    """
    Confirmação e remoção de Pet. Se POST, deleta e redireciona para listar_pets.
    """
    pet = get_object_or_404(Pet, id=pet_id)
    if request.method == 'POST':
        pet.delete()
        return redirect('listar_pets')
    return render(request, 'pets/remover_pet.html', {'pet': pet})

def pet_detalhe(request, pet_id):
    """
    Exibe detalhes de um Pet específico.
    """
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'pets/pet_detalhe.html', {'pet': pet})

def gerenciar_pets(request):
    """
    Área de gerenciamento: lista todos os pets, com formulário rápido para criar novo.
    """
    pets = Pet.objects.all()
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_pets')
    else:
        form = PetForm()
    return render(request, 'pets/gerenciar_pets.html', {
        'pets': pets,
        'form': form,
    })

def listar_animais_disponiveis(request):
    """
    Lista todos os pets (sem filtro de disponibilidade atualmente).
    Dependendo do template, talvez queira filtrar disponivel=True.
    """
    pets = Pet.objects.all()
    return render(request, 'pets/listar_animais.html', {'pets': pets})

@login_required(login_url='/contas/login/')
def adotar_pet(request, pet_id):
    """
    Processo de adoção:
    - Exibe formulário de adoção.
    - Se POST e válido, atribui pet, marca pet.indisponível e mostra mensagem de sucesso.
    """
    pet = get_object_or_404(Pet, pk=pet_id)

    if request.method == 'POST':
        form = AdocaoForm(request.POST, request.FILES)
        if form.is_valid():
            adocao = form.save(commit=False)
            adocao.pet = pet

            if request.user.is_authenticated:
                adocao.email_adotante = request.user.email

            adocao.save()

            pet.disponivel = False
            pet.save()

            return render(request, 'pets/adotar_pet.html', {
                'pet': pet,
                'form': AdocaoForm(),
                'msg_sucesso': 'Adoção confirmada com sucesso! Seus dados foram salvos.'
            })
    else:
        #Aqui preenche os dados automaticamente
        initial_data = {}
        if request.user.is_authenticated:
            perfil = Perfil.objects.filter(user=request.user).first()

            initial_data = {
                'nome_adotante': request.user.get_full_name() or request.user.username,
                'cpf_adotante': perfil.cpf if perfil else '',
                'rg_adotante': perfil.rg if perfil else '',
                'telefone_adotante': perfil.telefone if perfil else '',
            }

        form = AdocaoForm(initial=initial_data)

    return render(request, 'pets/adotar_pet.html', {'pet': pet, 'form': form})


@login_required
def meus_dados(request):
    """
    Exibe dados do usuário: perfil e possível adoção.
    Ajuste a lógica conforme relacionamento real (ex.: FK para User em Adocao).
    """
    user = request.user
    # Obtém ou cria perfil associado
    perfil = Perfil.objects.filter(user=user).first()
    adotacao = None

    # Exemplo de busca de adoção: pelo CPF do perfil ou e-mail
    if perfil and perfil.cpf:
        adotacao = Adocao.objects.filter(cpf_adotante=perfil.cpf).order_by('-data_adocao').first()
    if not adotacao:
        adotacao = Adocao.objects.filter(email_adotante=user.email).order_by('-data_adocao').first()

    return render(request, 'pets/meus_dados.html', {
        'user': user,
        'perfil': perfil,
        'adotacao': adotacao,
    })

@login_required
def meus_aumigos(request):
    """
    Lista todas as adoções feitas pelo usuário (filtradas por email).
    """
    aumigos = Adocao.objects.filter(email_adotante=request.user.email).select_related('pet')
    return render(request, 'pets/meus_aumigos.html', {'aumigos': aumigos})

@login_required
def editar_dados(request):
    """
    Permite que usuário edite seus dados (User e Perfil).
    Se POST válido, salva ambos e exibe mensagem de sucesso.
    """
    user = request.user
    perfil, _ = Perfil.objects.get_or_create(user=user)

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
    """
    Cancelamento de adoção:
    - Verifica se a adoção pertence ao usuário (pelo email).
    - Em POST, reabilita o pet e remove o registro de adoção.
    """
    adocao = get_object_or_404(Adocao, id=adocao_id)
    # checa propriedade
    if adocao.email_adotante != request.user.email:
        messages.error(request, 'Você não tem permissão para cancelar esta adoção.')
        return redirect('meus_aumigos')

    if request.method == 'POST':
        pet = adocao.pet
        pet.disponivel = True
        pet.save()
        adocao.delete()
        messages.success(request, 'Adoção cancelada com sucesso.')
        return redirect('meus_aumigos')

    return render(request, 'pets/cancelar_adocao_confirmar.html', {'adocao': adocao})