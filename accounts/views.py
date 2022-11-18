from django.contrib import auth, messages  # Mensagens
from django.contrib.auth.decorators import \
    login_required  # Quando a página precisa estar logado para acessar
from django.contrib.auth.models import \
    User  # Validar usuário e nome se já existe
from django.core.validators import validate_email  # Validar email
from django.shortcuts import redirect, render

from .models import FormContato  # importando o formulário no models

# Create your views here.

def login(request):
    if request.method !="POST":
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha) # Autenticar usuário e senha

    if not user:
        messages.error(request, 'Usuário ou senha inválidos')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user) # Logou
        messages.success(request, "Logado com sucesso")
        return redirect('dashboard')





def logout(request):
    auth.logout(request)
    return redirect('dashboard')





def register(request):
    print(request.POST) # Pegar com POST

    if request.method != 'POST':
        return render(request, 'accounts/register.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        messages.error(request, 'NENHUM CAMPO PODE ESTAR VAZIO')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido')
        return render(request, 'accounts/register.html')

    if len(senha) < 4:
        messages.error(request, 'Senha precisa ter 4 caracteres ou mais')
        return render(request, 'accounts/register.html')

    if len(usuario) < 3:
        messages.warning(request, 'Usuário precisa ter 3 caracteres ou mais')
        return render(request, 'accounts/register.html')

    if senha != senha2:
        messages.warning(request, 'Senha e confirmar senha não correspondem')
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuário já existe')
        return render(request, 'accounts/register.html')


    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email já existe')
        return render(request, 'accounts/register.html')
    
    messages.success(request, 'Usuário cadastrado')
    user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome, last_name=sobrenome)
    user.save()

    return redirect('login')



@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form}) # Enviando o formulário
        print('post')
    form = FormContato(request.POST, request.FILES) # Porque tem imagem
    print('validação')

    if not form.is_valid():
        print('Não valido')
        messages.error(request, 'Erro ao enviar ')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})
    print('salvar')
    form.save()
    print(form)
    return redirect('dashboard')
