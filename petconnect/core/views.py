from django.shortcuts import render, get_object_or_404
from .models import Pet, SolicitacaoAdocao, Favorito, Ong, Adotante, Usuario

def index(request):
    pets_destaque = Pet.objects.filter(status='disponivel')[:4]
    return render(request, 'core/index.html', {'pets_destaque': pets_destaque})

def listagem(request):
    pets = Pet.objects.all()
    # Aqui poderíamos aplicar filtros baseados no request.GET, mas para o MVP vamos retornar todos
    return render(request, 'core/listagem.html', {'pets': pets})

def detalhe(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'core/detalhe.html', {'pet': pet})

def cadastro(request):
    # Funcionalidade real não é exigida, apenas a tela e as tags Django
    return render(request, 'core/cadastro.html')

def painel_adotante(request):
    # Simulando um usuário adotante (no MVP podemos pegar o primeiro ou usar request.user)
    adotante = Adotante.objects.first()
    if adotante:
        pedidos = SolicitacaoAdocao.objects.filter(adotante=adotante)
        favoritos = Favorito.objects.filter(adotante=adotante)
    else:
        pedidos = []
        favoritos = []
        
    context = {
        'adotante': adotante,
        'pedidos': pedidos,
        'favoritos': favoritos,
    }
    return render(request, 'core/painel_adotante.html', context)

def solicitacoes_adocao(request):
    # Simulando um usuário ONG
    ong = Ong.objects.first()
    if ong:
        solicitacoes = SolicitacaoAdocao.objects.filter(pet__ong=ong).order_by('-data_solicitacao')
    else:
        solicitacoes = []
        
    context = {
        'ong': ong,
        'solicitacoes': solicitacoes,
    }
    return render(request, 'core/solicitacoes_adocao.html', context)

def editar_usuario(request):
    # Simula edição para o primeiro usuário
    usuario = Usuario.objects.first()
    return render(request, 'core/editar_usuario.html', {'usuario': usuario})
