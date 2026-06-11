from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pet, SolicitacaoAdocao, Favorito, Ong, Adotante, Usuario


# ═══════════════════════════════════════════════════════════
#  VIEWS PÚBLICAS — qualquer pessoa acessa
# ═══════════════════════════════════════════════════════════

def index(request):
    pets_destaque = Pet.objects.filter(status='disponivel')[:4]
    return render(request, 'core/index.html', {'pets_destaque': pets_destaque})


def listagem(request):
    pets = Pet.objects.all()
    return render(request, 'core/listagem.html', {'pets': pets})


def listagem_filtros(request):
    pets = Pet.objects.all()
    return render(request, 'core/listagem_filtros.html', {'pets': pets})


def busca_avancada(request):
    pets = Pet.objects.all()
    return render(request, 'core/busca_avancada.html', {'pets': pets})


def detalhe(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'core/detalhe.html', {'pet': pet})


def pagina_ong(request, ong_id):
    ong = get_object_or_404(Ong, id=ong_id)
    pets = Pet.objects.filter(ong=ong)
    return render(request, 'core/pagina_ong.html', {'ong': ong, 'pets': pets})


def recuperar_senha(request):
    return render(request, 'core/recuperar_senha.html')


# ═══════════════════════════════════════════════════════════
#  AUTENTICAÇÃO — login, cadastro, logout
# ═══════════════════════════════════════════════════════════

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email', '')
        senha = request.POST.get('senha', '')

        try:
            usuario = Usuario.objects.get(email=email)
            user = authenticate(request, username=usuario.username, password=senha)
        except Usuario.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            proximo = request.GET.get('next', '/')
            return redirect(proximo)
        else:
            messages.error(request, 'E-mail ou senha inválidos.')

    return render(request, 'core/login.html')


def cadastro_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        tipo = request.POST.get('user-type', 'adopter')
        email = request.POST.get('email', '')
        telefone = request.POST.get('phone', '')
        cidade = request.POST.get('city', '')
        estado = request.POST.get('state', '')
        senha = request.POST.get('password', '')
        confirma = request.POST.get('password-confirm', '')

        if not email or not senha:
            messages.error(request, 'Preencha todos os campos obrigatórios.')
            return render(request, 'core/cadastro.html')

        if senha != confirma:
            messages.error(request, 'As senhas não conferem.')
            return render(request, 'core/cadastro.html')

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Já existe uma conta com esse e-mail.')
            return render(request, 'core/cadastro.html')

        username = email.split('@')[0]
        base_username = username
        contador = 1
        while Usuario.objects.filter(username=username).exists():
            username = f'{base_username}{contador}'
            contador += 1

        tipo_usuario = 'ong' if tipo == 'ong' else 'adotante'

        usuario = Usuario.objects.create_user(
            username=username,
            email=email,
            password=senha,
            tipo=tipo_usuario,
            telefone=telefone,
            cidade=cidade,
            estado=estado,
        )

        if tipo == 'ong':
            nome_ong = request.POST.get('ong-name', '')
            cnpj = request.POST.get('cnpj', '')
            responsavel = request.POST.get('responsible', '')
            sobre = request.POST.get('about-ong', '')
            Ong.objects.create(
                usuario=usuario,
                nome_ong=nome_ong or f'ONG de {username}',
                cnpj=cnpj,
                responsavel=responsavel or username,
                sobre=sobre,
            )
        else:
            nome = request.POST.get('fullname', '')
            moradia = request.POST.get('housing', '')
            if nome:
                partes = nome.split(' ', 1)
                usuario.first_name = partes[0]
                if len(partes) > 1:
                    usuario.last_name = partes[1]
                usuario.save()
            Adotante.objects.create(
                usuario=usuario,
                tipo_moradia=moradia if moradia else None,
            )

        login(request, usuario)
        messages.success(request, 'Conta criada com sucesso! Bem-vindo ao PetConnect 🐾')
        return redirect('index')

    return render(request, 'core/cadastro.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


# ═══════════════════════════════════════════════════════════
#  VIEWS PROTEGIDAS — Qualquer usuário logado
# ═══════════════════════════════════════════════════════════

@login_required
def editar_usuario(request):
    return render(request, 'core/editar_usuario.html', {'usuario': request.user})


@login_required
def notificacoes(request):
    return render(request, 'core/notificacoes.html')


@login_required
def onboarding(request):
    return render(request, 'core/onboarding.html')


# ═══════════════════════════════════════════════════════════
#  VIEWS PROTEGIDAS — Adotante
# ═══════════════════════════════════════════════════════════

@login_required
def painel_adotante(request):
    if request.user.tipo != 'adotante':
        messages.error(request, 'Acesso restrito a adotantes.')
        return redirect('index')

    try:
        adotante = request.user.adotante_profile
    except Adotante.DoesNotExist:
        adotante = Adotante.objects.create(usuario=request.user)

    pedidos = SolicitacaoAdocao.objects.filter(adotante=adotante)
    favoritos = Favorito.objects.filter(adotante=adotante)

    context = {
        'adotante': adotante,
        'pedidos': pedidos,
        'favoritos': favoritos,
    }
    return render(request, 'core/painel_adotante.html', context)


@login_required
def favoritos(request):
    if request.user.tipo != 'adotante':
        return redirect('index')

    try:
        adotante = request.user.adotante_profile
    except Adotante.DoesNotExist:
        adotante = Adotante.objects.create(usuario=request.user)

    lista_favoritos = Favorito.objects.filter(adotante=adotante)
    return render(request, 'core/favoritos.html', {'favoritos': lista_favoritos, 'adotante': adotante})


@login_required
def perfil_adotante(request):
    if request.user.tipo != 'adotante':
        return redirect('index')

    try:
        adotante = request.user.adotante_profile
    except Adotante.DoesNotExist:
        adotante = Adotante.objects.create(usuario=request.user)

    return render(request, 'core/perfil_adotante.html', {'adotante': adotante})


@login_required
def historico_adocoes(request):
    if request.user.tipo != 'adotante':
        return redirect('index')

    try:
        adotante = request.user.adotante_profile
    except Adotante.DoesNotExist:
        adotante = Adotante.objects.create(usuario=request.user)

    adocoes = SolicitacaoAdocao.objects.filter(adotante=adotante, status='concluida')
    return render(request, 'core/historico_adocoes.html', {'adocoes': adocoes, 'adotante': adotante})


@login_required
def confirmacao_adocao(request, pet_id):
    if request.user.tipo != 'adotante':
        return redirect('index')

    pet = get_object_or_404(Pet, id=pet_id)

    try:
        adotante = request.user.adotante_profile
    except Adotante.DoesNotExist:
        adotante = Adotante.objects.create(usuario=request.user)

    solicitacao, created = SolicitacaoAdocao.objects.get_or_create(
        adotante=adotante,
        pet=pet,
        defaults={'status': 'pendente'}
    )

    if created:
        messages.success(request, f'Sua solicitação para adotar {pet.nome} foi enviada com sucesso! 🐾')
        # Atualiza status do pet para em análise
        if pet.status == 'disponivel':
            pet.status = 'analise'
            pet.save()

    return render(request, 'core/confirmacao_adocao.html', {'pet': pet, 'solicitacao': solicitacao})


@login_required
def termo_adocao(request, pet_id):
    if request.user.tipo != 'adotante':
        return redirect('index')

    pet = get_object_or_404(Pet, id=pet_id)

    try:
        adotante = request.user.adotante_profile
    except Adotante.DoesNotExist:
        return redirect('confirmacao_adocao', pet_id=pet_id)

    # Verifica se a solicitação existe e está aprovada
    try:
        solicitacao = SolicitacaoAdocao.objects.get(adotante=adotante, pet=pet)
    except SolicitacaoAdocao.DoesNotExist:
        messages.error(request, 'Você não tem uma solicitação ativa para este pet.')
        return redirect('confirmacao_adocao', pet_id=pet_id)

    if solicitacao.status not in ['aprovada', 'concluida']:
        messages.error(request, 'O termo de adoção só está disponível após a aprovação pela ONG.')
        return redirect('confirmacao_adocao', pet_id=pet_id)

    return render(request, 'core/termo_adocao.html', {'pet': pet, 'solicitacao': solicitacao})


@login_required
def assinar_termo(request, pet_id):
    """Processa a assinatura digital do termo e conclui a adoção."""
    if request.user.tipo != 'adotante':
        return redirect('index')

    if request.method != 'POST':
        return redirect('termo_adocao', pet_id=pet_id)

    pet = get_object_or_404(Pet, id=pet_id)

    try:
        adotante = request.user.adotante_profile
    except Adotante.DoesNotExist:
        messages.error(request, 'Perfil de adotante não encontrado.')
        return redirect('index')

    try:
        solicitacao = SolicitacaoAdocao.objects.get(adotante=adotante, pet=pet, status='aprovada')
    except SolicitacaoAdocao.DoesNotExist:
        messages.error(request, 'Solicitação não encontrada ou já concluída.')
        return redirect('confirmacao_adocao', pet_id=pet_id)

    # Valida que o adotante marcou as caixas e assinou
    check1 = request.POST.get('check1')
    check2 = request.POST.get('check2')
    check3 = request.POST.get('check3')
    assinado = request.POST.get('assinado', '0')

    if not (check1 and check2 and check3 and assinado == '1'):
        messages.error(request, 'Por favor, marque todas as confirmações e assine o documento.')
        return redirect('termo_adocao', pet_id=pet_id)

    # Conclui a adoção
    solicitacao.status = 'concluida'
    solicitacao.save()

    # Atualiza o status do pet para adotado
    pet.status = 'adotado'
    pet.save()

    messages.success(
        request,
        f'Parabéns! A adoção de {pet.nome} foi concluída com sucesso! '
        f'Que comecem as aventuras juntos 🎉🐾'
    )

    return redirect('confirmacao_adocao', pet_id=pet_id)


@login_required
def avaliar_ong(request, ong_id):
    if request.user.tipo != 'adotante':
        messages.error(request, 'Acesso restrito a adotantes.')
        return redirect('index')
    ong = get_object_or_404(Ong, id=ong_id)
    return render(request, 'core/avaliar_ong.html', {'ong': ong})


@login_required
def chat_ong(request, ong_id):
    ong = get_object_or_404(Ong, id=ong_id)
    return render(request, 'core/chat_ong.html', {'ong': ong})


# ═══════════════════════════════════════════════════════════
#  VIEWS PROTEGIDAS — ONG
# ═══════════════════════════════════════════════════════════

@login_required
def dashboard_ong(request):
    if request.user.tipo != 'ong':
        messages.error(request, 'Acesso restrito a ONGs.')
        return redirect('index')

    try:
        ong = request.user.ong_profile
    except Ong.DoesNotExist:
        messages.error(request, 'Perfil de ONG não encontrado.')
        return redirect('index')

    pets = Pet.objects.filter(ong=ong).order_by('-id')
    solicitacoes = SolicitacaoAdocao.objects.filter(
        pet__ong=ong
    ).select_related('adotante__usuario', 'pet').order_by('-data_solicitacao')[:5]

    # Estatísticas reais
    total_pets = pets.count()
    total_pendentes = SolicitacaoAdocao.objects.filter(pet__ong=ong, status='pendente').count()
    total_entrevista = SolicitacaoAdocao.objects.filter(pet__ong=ong, status='entrevista').count()
    total_adotados = pets.filter(status='adotado').count()
    total_disponiveis = pets.filter(status='disponivel').count()

    context = {
        'ong': ong,
        'pets': pets,
        'solicitacoes': solicitacoes,
        'total_pets': total_pets,
        'total_pendentes': total_pendentes,
        'total_entrevista': total_entrevista,
        'total_adotados': total_adotados,
        'total_disponiveis': total_disponiveis,
    }
    return render(request, 'core/dashboard_ong.html', context)


@login_required
def solicitacoes_adocao(request):
    if request.user.tipo != 'ong':
        messages.error(request, 'Acesso restrito a ONGs.')
        return redirect('index')

    try:
        ong = request.user.ong_profile
    except Ong.DoesNotExist:
        return redirect('index')

    solicitacoes = SolicitacaoAdocao.objects.filter(
        pet__ong=ong
    ).select_related('adotante__usuario', 'pet').order_by('-data_solicitacao')

    novas = solicitacoes.filter(status='pendente').count()
    entrevista = solicitacoes.filter(status='entrevista').count()
    aprovadas = solicitacoes.filter(status='aprovada').count()

    context = {
        'ong': ong,
        'solicitacoes': solicitacoes,
        'novas': '{:02d}'.format(novas),
        'entrevista': '{:02d}'.format(entrevista),
        'aprovadas': '{:02d}'.format(aprovadas),
    }
    return render(request, 'core/solicitacoes_adocao.html', context)


@login_required
def atualizar_solicitacao(request, sol_id, status):
    if request.user.tipo != 'ong':
        messages.error(request, 'Acesso restrito a ONGs.')
        return redirect('index')

    try:
        ong = request.user.ong_profile
    except Ong.DoesNotExist:
        return redirect('index')

    solicitacao = get_object_or_404(SolicitacaoAdocao, id=sol_id, pet__ong=ong)
    if status in dict(SolicitacaoAdocao.STATUS_CHOICES).keys():
        solicitacao.status = status
        solicitacao.save()
        messages.success(request, f'Status atualizado para {solicitacao.get_status_display()}.')

    return redirect('solicitacoes_adocao')


@login_required
def cadastro_pet(request):
    if request.user.tipo != 'ong':
        messages.error(request, 'Acesso restrito a ONGs.')
        return redirect('index')

    try:
        ong = request.user.ong_profile
    except Ong.DoesNotExist:
        return redirect('index')

    if request.method == 'POST':
        nome = request.POST.get('nome')
        especie = request.POST.get('especie')
        raca = request.POST.get('raca', 'SRD')
        sexo = request.POST.get('sexo')
        idade_texto = request.POST.get('idade')
        porte = request.POST.get('porte')
        descricao = request.POST.get('descricao')

        vacinado = request.POST.get('vacinado') == 'on'
        castrado = request.POST.get('castrado') == 'on'
        vermifugado = request.POST.get('vermifugado') == 'on'
        microchip = request.POST.get('microchip') == 'on'

        amigo_criancas = request.POST.get('amigo_criancas') == 'on'
        amigo_outros_pets = request.POST.get('amigo_outros_pets') == 'on'

        if nome and especie and sexo and idade_texto and porte:
            Pet.objects.create(
                ong=ong,
                nome=nome,
                especie=especie,
                raca=raca,
                sexo=sexo,
                idade_texto=idade_texto,
                porte=porte,
                descricao=descricao,
                vacinado=vacinado,
                castrado=castrado,
                vermifugado=vermifugado,
                microchip=microchip,
                amigo_criancas=amigo_criancas,
                amigo_outros_pets=amigo_outros_pets,
                status='disponivel'
            )
            messages.success(request, 'Pet cadastrado com sucesso!')
            return redirect('dashboard_ong')
        else:
            messages.error(request, 'Preencha todos os campos obrigatórios.')

    return render(request, 'core/cadastro_pet.html', {'ong': ong})


@login_required
def lar_temporario(request):
    if request.user.tipo != 'ong':
        messages.error(request, 'Acesso restrito a ONGs.')
        return redirect('index')

    try:
        ong = request.user.ong_profile
    except Ong.DoesNotExist:
        return redirect('index')

    return render(request, 'core/lar_temporario.html', {'ong': ong})


@login_required
def cadastro_ong(request):
    if request.user.tipo != 'ong':
        return redirect('index')

    return render(request, 'core/cadastro_ong.html')
