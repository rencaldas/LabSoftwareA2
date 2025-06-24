from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from sistema_projeto.pets.models import Perfil
from sistema_projeto.pets.models import Pet
# from .utils import is_admin  # removido, pois não estava sendo usado


def login_view(request):
    """
    View para processar login de usuário via e-mail e senha.
    - Se GET: exibe o formulário de login.
    - Se POST: busca usuário pelo e-mail, tenta autenticar e redireciona.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        # parâmetro 'next' para redirecionar após login. default para home ('/')
        next_url = request.GET.get('next', '/')
        # Tenta obter usuário a partir do email fornecido
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            # Email não existe; renderiza template com erro
            return render(request, 'contas/login.html', {'erro': 'Email não encontrado'})

        # Se achou user_obj, tenta autenticar usando username dele e senha informada
        user = authenticate(request, username=user_obj.username, password=senha)
        if user is not None:
            # Autenticado com sucesso: faz login e redireciona
            login(request, user)
            return redirect(next_url)
        else:
            # Senha incorreta ou outra falha de autenticação
            return render(request, 'contas/login.html', {'erro': 'Credenciais inválidas'})
    else:
        # GET: apenas renderiza o formulário de login
        return render(request, 'contas/login.html')


def cadastro_view(request):
    """
    View para cadastro de novo usuário via e-mail e senha.
    - Se GET: exibe o formulário de cadastro.
    - Se POST: valida senhas, verifica existência de email, cria usuário e faz login.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')  # Novo campo: nome de usuário
        first_name = request.POST.get('first_name')  # Novo campo: primeiro nome
        last_name = request.POST.get('last_name')  # Novo campo: sobrenome
        telefone = request.POST.get('telefone')  # Novo campo: telefone (vai para o modelo Perfil)

        senha = request.POST.get('senha')
        confirmacao = request.POST.get('confirmar_senha')

        # Verifica se senhas coincidem
        if senha != confirmacao:
            return render(request, 'contas/cadastro.html', {'erro': 'Senhas não coincidem'})

        # Verifica se já existe usuário com este email
        if User.objects.filter(email=email).exists():
            return render(request, 'contas/cadastro.html', {'erro': 'Email já cadastrado'})

        # Verifica se já existe usuário com este username
        if User.objects.filter(username=username).exists():
            return render(request, 'contas/cadastro.html', {'erro': 'Nome de usuário já cadastrado'})

        # Cria usuário
        usuario = User.objects.create_user(
            username=username if username else email,  # Usa username informado, se não, o email
            email=email,
            password=senha,
            first_name=first_name,
            last_name=last_name
        )

        # Cria perfil vinculado ao usuário
        Perfil.objects.create(
            user=usuario,
            telefone=telefone  # Salva telefone no perfil
        )

        # Faz login automático após cadastro
        login(request, usuario)
        return redirect('/')
    else:
        # GET: renderiza o formulário de cadastro
        return render(request, 'contas/cadastro.html')


def logout_view(request):
    """
    View para logout de usuário.
    - Sempre redireciona para a página inicial após logout.
    """
    logout(request)
    return redirect('/')


@login_required
def gerenciar_pets_view(request):
    """
    View para exibir todos os pets (requer login).
    - Atualmente lista todos os pets cadastrados.
    - Caso queira filtrar por usuário ou outra regra, ajustar aqui.
    """
    pets = Pet.objects.all().order_by('id')
    context = {'pets': pets}
    return render(request, 'contas/gerenciar_pets.html', context)