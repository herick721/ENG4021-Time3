from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db.models import Q, Avg, Count
from .models import Pet, PetImage, SolicitacaoAdocao, Favorito, Ong, Adotante, Usuario, Parceiro, Banner, Vacina, Notificacao, Avaliacao


# ═══════════════════════════════════════════════════════════
#  VIEWS PÚBLICAS — qualquer pessoa acessa
# ═══════════════════════════════════════════════════════════

def index(request):
    pets_destaque = Pet.objects.filter(status='disponivel')[:4]
    banners = Banner.objects.filter(ativo=True)
    stats = {
        'pets': Pet.objects.count(),
        'ongs': Ong.objects.count(),
        'adocoes': SolicitacaoAdocao.objects.filter(status='concluida').count(),
        'parceiros': Parceiro.objects.filter(ativo=True).count(),
    }
    return render(request, 'core/index.html', {
        'pets_destaque': pets_destaque,
        'banners': banners,
        'stats': stats,
    })


def listagem(request):
    pets = Pet.objects.filter(status='disponivel').select_related('ong__usuario')
    return render(request, 'core/listagem.html', {'pets': pets})


def listagem_filtros(request):
    pets = Pet.objects.filter(status='disponivel').select_related('ong__usuario')

    especie = request.GET.get('especie')
    porte = request.GET.get('porte')
    sexo = request.GET.get('sexo')
    cidade = request.GET.get('cidade')

    if especie in dict(Pet.ESPECIE_CHOICES).keys():
        pets = pets.filter(especie=especie)
    if porte in dict(Pet.PORTE_CHOICES).keys():
        pets = pets.filter(porte=porte)
    if sexo in dict(Pet.SEXO_CHOICES).keys():
        pets = pets.filter(sexo=sexo)
    if cidade:
        pets = pets.filter(ong__usuario__cidade__icontains=cidade)

    return render(request, 'core/listagem_filtros.html', {'pets': pets})


def busca_avancada(request):
    pets = Pet.objects.filter(status='disponivel').select_related('ong__usuario')

    q = request.GET.get('q', '')
    especie = request.GET.get('especie')
    porte = request.GET.get('porte')
    sexo = request.GET.get('sexo')
    vacinado = request.GET.get('vacinado')

    if q:
        pets = pets.filter(
            Q(nome__icontains=q) | Q(raca__icontains=q) | Q(descricao__icontains=q)
        )
    if especie in dict(Pet.ESPECIE_CHOICES).keys():
        pets = pets.filter(especie=especie)
    if porte in dict(Pet.PORTE_CHOICES).keys():
        pets = pets.filter(porte=porte)
    if sexo in dict(Pet.SEXO_CHOICES).keys():
        pets = pets.filter(sexo=sexo)
    if vacinado == 'sim':
        pets = pets.filter(vacinado=True)

    return render(request, 'core/busca_avancada.html', {'pets': pets})


def detalhe(request, pet_id):
    pet = get_object_or_404(Pet.objects.select_related('ong__usuario'), id=pet_id)
    imagens = pet.imagens.all()
    return render(request, 'core/detalhe.html', {'pet': pet, 'imagens': imagens})


def pagina_ong(request, ong_id):
    ong = get_object_or_404(Ong, id=ong_id)
    pets = Pet.objects.filter(ong=ong).prefetch_related('imagens')
    avaliacoes = Avaliacao.objects.filter(ong=ong)
    media_avaliacao = avaliacoes.aggregate(media=Avg('nota'))['media']
    total_avaliacoes = avaliacoes.count()
    total_adocoes = SolicitacaoAdocao.objects.filter(pet__ong=ong, status='concluida').count()
    total_pets_ong = pets.count()
    return render(request, 'core/pagina_ong.html', {
        'ong': ong,
        'pets': pets,
        'media_avaliacao': media_avaliacao,
        'total_avaliacoes': total_avaliacoes,
        'total_adocoes': total_adocoes,
        'total_pets_ong': total_pets_ong,
    })


def recuperar_senha(request):
    return render(request, 'core/recuperar_senha.html')


# ═══════════════════════════════════════════════════════════
#  AUTENTICAÇÃO — login, cadastro, logout
# ═══════════════════════════════════════════════════════════

def login_view(request):
    # Se já está logado, redireciona para a home
    if request.user.is_authenticated:
        return redirect('index')

    error_type = None  # 'not_found' or 'wrong_password'

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        senha = request.POST.get('senha', '')

        # O Django autentica por username, mas nosso login é por email
        # Então buscamos o usuário pelo email e usamos o username dele
        try:
            usuario = Usuario.objects.get(email=email)
            user = authenticate(request, username=usuario.username, password=senha)
            if user is not None:
                login(request, user)
                proximo = request.GET.get('next', '/')
                return redirect(proximo)
            else:
                # Usuário existe mas a senha está errada
                error_type = 'wrong_password'
        except Usuario.DoesNotExist:
            # Nenhum usuário com esse e-mail
            error_type = 'not_found'

    return render(request, 'core/login.html', {'error_type': error_type, 'email': request.POST.get('email', '') if request.method == 'POST' else ''})


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
        step = request.POST.get('current_step', '3')

        # Validações básicas
        if not email or not senha:
            messages.error(request, 'Preencha todos os campos obrigatórios.')
            return render(request, 'core/cadastro.html', {'form': request.POST, 'current_step': step, 'tipo': tipo})

        if '@' not in email:
            messages.error(request, 'Digite um e-mail válido (com @).')
            return render(request, 'core/cadastro.html', {'form': request.POST, 'current_step': step, 'tipo': tipo})

        if len(senha) < 6:
            messages.error(request, 'A senha deve ter pelo menos 6 caracteres.')
            return render(request, 'core/cadastro.html', {'form': request.POST, 'current_step': step, 'tipo': tipo})

        if senha != confirma:
            messages.error(request, 'As senhas não conferem.')
            return render(request, 'core/cadastro.html', {'form': request.POST, 'current_step': step, 'tipo': tipo})

        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Já existe uma conta com esse e-mail.')
            return render(request, 'core/cadastro.html', {'form': request.POST, 'current_step': step, 'tipo': tipo})

        # Cria o usuário (username = parte antes do @ do email)
        username = email.split('@')[0]
        # Garante username único
        base_username = username
        contador = 1
        while Usuario.objects.filter(username=username).exists():
            username = f'{base_username}{contador}'
            contador += 1

        if tipo == 'ong':
            tipo_usuario = 'ong'
        else:
            tipo_usuario = 'adotante'

        usuario = Usuario.objects.create_user(
            username=username,
            email=email,
            password=senha,
            tipo=tipo_usuario,
            telefone=telefone,
            cidade=cidade,
            estado=estado,
        )

        # Cria o perfil específico
        try:
            if tipo == 'ong':
                nome_ong = request.POST.get('ong_name', '').strip()
                cnpj = request.POST.get('cnpj', '').strip()
                responsavel = request.POST.get('responsible', '').strip()
                sobre = request.POST.get('about_ong', '').strip()
                # Valida CNPJ (mínimo 14 dígitos)
                if cnpj:
                    cnpj_limpo = cnpj.replace('.', '').replace('/', '').replace('-', '')
                    if not cnpj_limpo.isdigit() or len(cnpj_limpo) < 14:
                        messages.error(request, 'CNPJ inválido. Use o formato 00.000.000/0001-00.')
                        usuario.delete()
                        return render(request, 'core/cadastro.html', {'form': request.POST, 'current_step': step, 'tipo': tipo})
                Ong.objects.create(
                    usuario=usuario,
                    nome_ong=nome_ong or f'ONG de {username}',
                    cnpj=cnpj if cnpj else None,
                    responsavel=responsavel or username,
                    sobre=sobre if sobre else None,
                )
            else:
                nome = request.POST.get('fullname', '').strip()
                moradia = request.POST.get('housing', '')
                idade = request.POST.get('idade', '').strip()
                ocupacao = request.POST.get('ocupacao', '').strip()
                moradores = request.POST.get('moradores', '').strip()
                # Valida idade
                if idade and idade.isdigit():
                    idade_int = int(idade)
                    if idade_int < 18 or idade_int > 120:
                        messages.error(request, 'A idade deve estar entre 18 e 120 anos.')
                        usuario.delete()
                        return render(request, 'core/cadastro.html', {'form': request.POST, 'current_step': step, 'tipo': tipo})
                if nome:
                    partes = nome.split(' ', 1)
                    usuario.first_name = partes[0]
                    if len(partes) > 1:
                        usuario.last_name = partes[1]
                    usuario.save()
                Adotante.objects.create(
                    usuario=usuario,
                    tipo_moradia=moradia if moradia else None,
                    idade=int(idade) if idade and idade.isdigit() else None,
                    ocupacao=ocupacao if ocupacao else None,
                    moradores=moradores if moradores else None,
                )
        except Exception as e:
            # Se algo falhar ao criar o perfil, remove o usuário e mostra o erro
            usuario.delete()
            messages.error(request, f'Erro ao criar o perfil: {e}')
            return render(request, 'core/cadastro.html', {'form': request.POST, 'current_step': step, 'tipo': tipo})

        # Faz login automático após cadastro
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
    if request.method == 'POST':
        fullname = request.POST.get('fullname', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip().upper()

        if fullname:
            partes = fullname.split(' ', 1)
            request.user.first_name = partes[0]
            request.user.last_name = partes[1] if len(partes) > 1 else ''
        if email and email != request.user.email:
            if Usuario.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.error(request, 'Este e-mail já está em uso.')
                return render(request, 'core/editar_usuario.html', {'usuario': request.user})
            request.user.email = email

        request.user.telefone = phone
        request.user.cidade = city
        request.user.estado = state[:2] if state else ''
        request.user.save()
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('editar_usuario')

    return render(request, 'core/editar_usuario.html', {'usuario': request.user})


@login_required
def notificacoes(request):
    notificacoes_lista = Notificacao.objects.filter(usuario=request.user).select_related('usuario')
    nao_lidas = notificacoes_lista.filter(lida=False).count()
    return render(request, 'core/notificacoes.html', {
        'notificacoes': notificacoes_lista,
        'nao_lidas': nao_lidas,
    })


@login_required
def onboarding(request):
    return render(request, 'core/onboarding.html')


# ═══════════════════════════════════════════════════════════
#  VIEWS PROTEGIDAS — Adotante
# ═══════════════════════════════════════════════════════════

@login_required
def painel_adotante(request):
    # Verifica se o usuário é adotante
    if request.user.tipo != 'adotante':
        messages.error(request, 'Acesso restrito a adotantes.')
        return redirect('index')

    try:
        adotante = request.user.adotante_profile
    except Adotante.DoesNotExist:
        # Se o perfil não existe ainda, cria um básico
        adotante = Adotante.objects.create(usuario=request.user)

    pedidos = SolicitacaoAdocao.objects.filter(adotante=adotante).select_related('pet__ong__usuario')
    favoritos = Favorito.objects.filter(adotante=adotante).select_related('pet__ong__usuario')

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

    lista_favoritos = Favorito.objects.filter(adotante=adotante).select_related('pet__ong__usuario')
    return render(request, 'core/favoritos.html', {'favoritos': lista_favoritos, 'adotante': adotante})


@login_required
def toggle_favorito(request, pet_id):
    if request.user.tipo != 'adotante':
        messages.error(request, 'Acesso restrito a adotantes.')
        return redirect('index')

    try:
        adotante = request.user.adotante_profile
    except Adotante.DoesNotExist:
        adotante = Adotante.objects.create(usuario=request.user)

    pet = get_object_or_404(Pet, id=pet_id)

    if request.method == 'POST':
        favorito = Favorito.objects.filter(adotante=adotante, pet=pet).first()
        if favorito:
            favorito.delete()
            messages.success(request, f'{pet.nome} removido dos favoritos.')
        else:
            Favorito.objects.create(adotante=adotante, pet=pet)
            messages.success(request, f'{pet.nome} adicionado aos favoritos!')

    return redirect(request.META.get('HTTP_REFERER', 'index'))


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

    adocoes = SolicitacaoAdocao.objects.filter(adotante=adotante, status='concluida').select_related('pet__ong__usuario')
    return render(request, 'core/historico_adocoes.html', {'adocoes': adocoes, 'adotante': adotante})


@login_required
def confirmacao_adocao(request, pet_id):
    if request.user.tipo != 'adotante':
        return redirect('index')

    pet = get_object_or_404(Pet, id=pet_id)

    # Só cria a solicitação via POST (evita criação acidental em GET)
    if request.method == 'POST':
        try:
            adotante = request.user.adotante_profile
        except Adotante.DoesNotExist:
            adotante = Adotante.objects.create(usuario=request.user)

        solicitacao, created = SolicitacaoAdocao.objects.get_or_create(
            adotante=adotante,
            pet=pet,
            defaults={'status': 'pendente'}
        )

        return render(request, 'core/confirmacao_adocao.html', {'pet': pet, 'solicitacao': solicitacao})

    return redirect('detalhe', pet_id=pet_id)


@login_required
def termo_adocao(request, pet_id):
    if request.user.tipo != 'adotante':
        return redirect('index')

    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'core/termo_adocao.html', {'pet': pet})


@login_required
def avaliar_ong(request, ong_id):
    if request.user.tipo != 'adotante':
        messages.error(request, 'Acesso restrito a adotantes.')
        return redirect('index')

    ong = get_object_or_404(Ong, id=ong_id)

    try:
        adotante = request.user.adotante_profile
    except Adotante.DoesNotExist:
        adotante = Adotante.objects.create(usuario=request.user)

    avaliacao_existente = Avaliacao.objects.filter(ong=ong, adotante=adotante).first()

    if request.method == 'POST':
        nota = request.POST.get('nota')
        comentario = request.POST.get('comentario', '').strip()

        if not nota or not nota.isdigit() or int(nota) < 1 or int(nota) > 5:
            messages.error(request, 'Selecione uma nota entre 1 e 5.')
            return redirect('avaliar_ong', ong_id=ong.id)

        if avaliacao_existente:
            avaliacao_existente.nota = int(nota)
            avaliacao_existente.comentario = comentario
            avaliacao_existente.save()
            messages.success(request, 'Sua avaliação foi atualizada!')
        else:
            Avaliacao.objects.create(
                ong=ong,
                adotante=adotante,
                nota=int(nota),
                comentario=comentario,
            )
            messages.success(request, 'Avaliação enviada com sucesso!')

        return redirect('pagina_ong', ong_id=ong.id)

    return render(request, 'core/avaliar_ong.html', {
        'ong': ong,
        'avaliacao_existente': avaliacao_existente,
    })


@login_required
def chat_ong(request, ong_id):
    if request.user.tipo != 'adotante':
        messages.error(request, 'Acesso restrito a adotantes.')
        return redirect('index')
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

    pets = Pet.objects.filter(ong=ong).prefetch_related('imagens')
    solicitacoes = SolicitacaoAdocao.objects.filter(pet__ong=ong).select_related('adotante__usuario', 'pet').order_by('-data_solicitacao')[:5]
    total_pets = pets.count()
    total_adocoes = SolicitacaoAdocao.objects.filter(pet__ong=ong, status='concluida').count()

    context = {
        'ong': ong,
        'pets': pets,
        'solicitacoes': solicitacoes,
        'total_pets': total_pets,
        'total_adocoes': total_adocoes,
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

    solicitacoes = SolicitacaoAdocao.objects.filter(pet__ong=ong).select_related('adotante__usuario', 'pet').order_by('-data_solicitacao')
    
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
def atualizar_solicitacao(request, sol_id):
    if request.user.tipo != 'ong':
        messages.error(request, 'Acesso restrito a ONGs.')
        return redirect('index')

    try:
        ong = request.user.ong_profile
    except Ong.DoesNotExist:
        return redirect('index')

    if request.method != 'POST':
        return redirect('solicitacoes_adocao')

    solicitacao = get_object_or_404(SolicitacaoAdocao, id=sol_id, pet__ong=ong)
    novo_status = request.POST.get('status', '')

    if novo_status in dict(SolicitacaoAdocao.STATUS_CHOICES).keys():
        solicitacao.status = novo_status
        if novo_status == 'recusada':
            solicitacao.motivo_recusa = request.POST.get('motivo_recusa', '')
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
            # Valida choices contra o model
            if especie not in dict(Pet.ESPECIE_CHOICES):
                messages.error(request, 'Espécie inválida.')
                return render(request, 'core/cadastro_pet.html', {'ong': ong})
            if sexo not in dict(Pet.SEXO_CHOICES):
                messages.error(request, 'Sexo inválido.')
                return render(request, 'core/cadastro_pet.html', {'ong': ong})
            if porte not in dict(Pet.PORTE_CHOICES):
                messages.error(request, 'Porte inválido.')
                return render(request, 'core/cadastro_pet.html', {'ong': ong})

            pet = Pet.objects.create(
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
            # Salva imagens enviadas
            for i in range(3):
                campo = f'imagem_{i}'
                if campo in request.FILES:
                    PetImage.objects.create(pet=pet, imagem=request.FILES[campo], ordem=i)
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
def editar_pet(request, pet_id):
    if request.user.tipo != 'ong':
        messages.error(request, 'Acesso restrito a ONGs.')
        return redirect('index')

    try:
        ong = request.user.ong_profile
    except Ong.DoesNotExist:
        return redirect('index')

    pet = get_object_or_404(Pet, id=pet_id, ong=ong)

    if request.method == 'POST':
        # Valida choices contra o model
        especie = request.POST.get('especie', pet.especie)
        sexo = request.POST.get('sexo', pet.sexo)
        porte = request.POST.get('porte', pet.porte)
        status = request.POST.get('status', pet.status)

        if especie not in dict(Pet.ESPECIE_CHOICES):
            messages.error(request, 'Espécie inválida.')
            return redirect('editar_pet', pet_id=pet.id)
        if sexo not in dict(Pet.SEXO_CHOICES):
            messages.error(request, 'Sexo inválido.')
            return redirect('editar_pet', pet_id=pet.id)
        if porte not in dict(Pet.PORTE_CHOICES):
            messages.error(request, 'Porte inválido.')
            return redirect('editar_pet', pet_id=pet.id)
        if status not in dict(Pet.STATUS_CHOICES):
            messages.error(request, 'Status inválido.')
            return redirect('editar_pet', pet_id=pet.id)

        pet.especie = especie
        pet.sexo = sexo
        pet.porte = porte
        pet.status = status
        pet.nome = request.POST.get('nome', pet.nome)
        pet.raca = request.POST.get('raca', pet.raca)
        pet.idade_texto = request.POST.get('idade', pet.idade_texto)
        pet.descricao = request.POST.get('descricao', pet.descricao)
        pet.vacinado = request.POST.get('vacinado') == 'on'
        pet.castrado = request.POST.get('castrado') == 'on'
        pet.vermifugado = request.POST.get('vermifugado') == 'on'
        pet.microchip = request.POST.get('microchip') == 'on'
        pet.amigo_criancas = request.POST.get('amigo_criancas') == 'on'
        pet.amigo_outros_pets = request.POST.get('amigo_outros_pets') == 'on'
        pet.urgente = request.POST.get('urgente') == 'on'
        pet.save()

        # Atualiza imagens
        for i in range(3):
            campo = f'imagem_{i}'
            if campo in request.FILES:
                img_qs = pet.imagens.filter(ordem=i)
                if img_qs.exists():
                    img = img_qs.first()
                    img.imagem = request.FILES[campo]
                    img.save()
                else:
                    PetImage.objects.create(pet=pet, imagem=request.FILES[campo], ordem=i)

        messages.success(request, f'{pet.nome} atualizado com sucesso!')
        return redirect('dashboard_ong')

    return render(request, 'core/cadastro_pet.html', {'ong': ong, 'pet': pet})


@login_required
def excluir_pet(request, pet_id):
    if request.user.tipo != 'ong':
        messages.error(request, 'Acesso restrito a ONGs.')
        return redirect('index')

    try:
        ong = request.user.ong_profile
    except Ong.DoesNotExist:
        return redirect('index')

    pet = get_object_or_404(Pet, id=pet_id, ong=ong)

    if request.method == 'POST':
        nome = pet.nome
        pet.delete()
        messages.success(request, f'{nome} removido permanentemente.')
        return redirect('dashboard_ong')

    return render(request, 'core/excluir_pet.html', {'pet': pet})


@login_required
def cadastro_ong(request):
    if request.user.tipo != 'ong':
        return redirect('index')

    try:
        ong = request.user.ong_profile
    except Ong.DoesNotExist:
        return redirect('index')

    if request.method == 'POST':
        ong.nome_ong = request.POST.get('nome_ong', ong.nome_ong)
        ong.cnpj = request.POST.get('cnpj', ong.cnpj)
        ong.responsavel = request.POST.get('responsavel', ong.responsavel)
        ong.sobre = request.POST.get('descricao', ong.sobre)
        ong.maps_url = request.POST.get('maps_url', ong.maps_url)
        ong.save()
        messages.success(request, 'Perfil da ONG atualizado!')
        return redirect('cadastro_ong')

    return render(request, 'core/cadastro_ong.html', {'ong': ong})


# ═══════════════════════════════════════════════════════════
#  PÁGINAS ESTÁTICAS / INFORMAÇÃO
# ═══════════════════════════════════════════════════════════

def como_funciona(request):
    return render(request, 'core/como_funciona.html')


def contato(request):
    return render(request, 'core/contato.html')


def pos_adocao(request):
    return render(request, 'core/pos_adocao.html')


@login_required
def configuracoes_seguranca(request):
    if request.method == 'POST':
        senha_atual = request.POST.get('senha_atual', '')
        nova_senha = request.POST.get('nova_senha', '')
        confirmar_senha = request.POST.get('confirmar_senha', '')

        if not request.user.check_password(senha_atual):
            messages.error(request, 'Senha atual incorreta.')
            return render(request, 'core/configuracoes_seguranca.html')

        if not nova_senha:
            messages.error(request, 'A nova senha não pode ficar em branco.')
            return render(request, 'core/configuracoes_seguranca.html')

        if nova_senha != confirmar_senha:
            messages.error(request, 'As senhas não conferem.')
            return render(request, 'core/configuracoes_seguranca.html')

        try:
            validate_password(nova_senha, user=request.user)
        except ValidationError as e:
            for msg in e.messages:
                messages.error(request, msg)
            return render(request, 'core/configuracoes_seguranca.html')

        request.user.set_password(nova_senha)
        request.user.save()

        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Senha alterada com sucesso!')
        return redirect('configuracoes_seguranca')

    return render(request, 'core/configuracoes_seguranca.html')


@login_required
def excluir_conta(request):
    if request.method == 'POST':
        usuario = request.user
        usuario.delete()
        messages.success(request, 'Conta excluída com sucesso.')
        return redirect('index')
    return render(request, 'core/excluir_conta.html')


@login_required
def relatorio_ong(request):
    if request.user.tipo != 'ong':
        messages.error(request, 'Acesso restrito a ONGs.')
        return redirect('index')

    try:
        ong = request.user.ong_profile
    except Ong.DoesNotExist:
        return redirect('index')

    total_pets = Pet.objects.filter(ong=ong).count()
    disponiveis = Pet.objects.filter(ong=ong, status='disponivel').count()
    adotados = Pet.objects.filter(ong=ong, status='adotado').count()
    em_processo = Pet.objects.filter(ong=ong, status__in=['analise', 'entrevista']).count()

    total_solicitacoes = SolicitacaoAdocao.objects.filter(pet__ong=ong).count()
    solicitacoes_pendentes = SolicitacaoAdocao.objects.filter(pet__ong=ong, status='pendente').count()
    solicitacoes_concluidas = SolicitacaoAdocao.objects.filter(pet__ong=ong, status='concluida').count()
    solicitacoes_recusadas = SolicitacaoAdocao.objects.filter(pet__ong=ong, status='recusada').count()

    taxa_adocao = round((adotados / total_pets * 100), 1) if total_pets > 0 else 0
    taxa_sucesso = round((solicitacoes_concluidas / total_solicitacoes * 100), 1) if total_solicitacoes > 0 else 0

    return render(request, 'core/relatorio_ong.html', {
        'ong': ong,
        'total_pets': total_pets,
        'disponiveis': disponiveis,
        'adotados': adotados,
        'em_processo': em_processo,
        'total_solicitacoes': total_solicitacoes,
        'solicitacoes_pendentes': solicitacoes_pendentes,
        'solicitacoes_concluidas': solicitacoes_concluidas,
        'solicitacoes_recusadas': solicitacoes_recusadas,
        'taxa_adocao': taxa_adocao,
        'taxa_sucesso': taxa_sucesso,
    })


# ═══════════════════════════════════════════════════════════
#  PARCEIROS / AFILIADOS
# ═══════════════════════════════════════════════════════════

def parceiros(request):
    parceiros = Parceiro.objects.filter(ativo=True)
    return render(request, 'core/parceiros.html', {'parceiros': parceiros})


@login_required
def admin_parceiros(request):
    if not request.user.is_staff:
        messages.error(request, 'Acesso restrito à equipe PetConnect.')
        return redirect('index')
    lista = Parceiro.objects.all().order_by('-data_criacao')
    return render(request, 'core/admin_parceiros.html', {'parceiros': lista})


@login_required
def admin_parceiro_adicionar(request):
    if not request.user.is_staff:
        return redirect('index')

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        descricao = request.POST.get('descricao_curta', '').strip()
        imagem = request.POST.get('imagem', '').strip()
        link = request.POST.get('link_externo', '').strip()
        tipo = request.POST.get('tipo', 'produto')
        ativo = request.POST.get('ativo') == 'on'

        if not nome or not descricao or not link:
            messages.error(request, 'Preencha todos os campos obrigatórios.')
        else:
            Parceiro.objects.create(
                nome=nome,
                descricao_curta=descricao,
                imagem=imagem or '🤝',
                link_externo=link,
                tipo=tipo,
                ativo=ativo,
            )
            messages.success(request, f'Parceiro "{nome}" cadastrado com sucesso!')
            return redirect('admin_parceiros')

    return render(request, 'core/admin_parceiro_form.html', {'acao': 'Adicionar'})


@login_required
def admin_parceiro_editar(request, parceiro_id):
    if not request.user.is_staff:
        return redirect('index')

    parceiro = get_object_or_404(Parceiro, id=parceiro_id)

    if request.method == 'POST':
        parceiro.nome = request.POST.get('nome', parceiro.nome).strip()
        parceiro.descricao_curta = request.POST.get('descricao_curta', parceiro.descricao_curta).strip()
        parceiro.imagem = request.POST.get('imagem', parceiro.imagem).strip()
        parceiro.link_externo = request.POST.get('link_externo', parceiro.link_externo).strip()
        parceiro.tipo = request.POST.get('tipo', parceiro.tipo)
        parceiro.ativo = request.POST.get('ativo') == 'on'

        if not parceiro.nome or not parceiro.descricao_curta or not parceiro.link_externo:
            messages.error(request, 'Preencha todos os campos obrigatórios.')
        else:
            parceiro.save()
            messages.success(request, f'Parceiro "{parceiro.nome}" atualizado!')
            return redirect('admin_parceiros')

    return render(request, 'core/admin_parceiro_form.html', {'parceiro': parceiro, 'acao': 'Editar'})


@login_required
def admin_parceiro_excluir(request, parceiro_id):
    if not request.user.is_staff:
        return redirect('index')

    parceiro = get_object_or_404(Parceiro, id=parceiro_id)

    if request.method == 'POST':
        nome = parceiro.nome
        parceiro.delete()
        messages.success(request, f'Parceiro "{nome}" removido.')
        return redirect('admin_parceiros')

    return render(request, 'core/admin_parceiro_excluir.html', {'parceiro': parceiro})


# ═══════════════════════════════════════════════════════════
#  BANNERS (Carrossel da Home)
# ═══════════════════════════════════════════════════════════

@login_required
def admin_banners(request):
    if not request.user.is_staff:
        return redirect('index')
    banners = Banner.objects.all()
    return render(request, 'core/admin_banners.html', {'banners': banners})


@login_required
def admin_banner_adicionar(request):
    if not request.user.is_staff:
        return redirect('index')

    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        ativo = request.POST.get('ativo') == 'on'
        ordem = request.POST.get('ordem', 0)

        if not titulo or 'imagem' not in request.FILES:
            messages.error(request, 'Preencha o título e selecione uma imagem.')
        else:
            Banner.objects.create(
                titulo=titulo,
                imagem=request.FILES['imagem'],
                ativo=ativo,
                ordem=ordem,
            )
            messages.success(request, 'Banner cadastrado!')
            return redirect('admin_banners')

    return render(request, 'core/admin_banner_form.html', {'acao': 'Adicionar'})


@login_required
def admin_banner_editar(request, banner_id):
    if not request.user.is_staff:
        return redirect('index')

    banner = get_object_or_404(Banner, id=banner_id)

    if request.method == 'POST':
        banner.titulo = request.POST.get('titulo', banner.titulo).strip()
        banner.ativo = request.POST.get('ativo') == 'on'
        banner.ordem = request.POST.get('ordem', banner.ordem)

        if 'imagem' in request.FILES:
            banner.imagem = request.FILES['imagem']

        if not banner.titulo:
            messages.error(request, 'O título é obrigatório.')
        else:
            banner.save()
            messages.success(request, 'Banner atualizado!')
            return redirect('admin_banners')

    return render(request, 'core/admin_banner_form.html', {'banner': banner, 'acao': 'Editar'})


@login_required
def admin_banner_excluir(request, banner_id):
    if not request.user.is_staff:
        return redirect('index')

    banner = get_object_or_404(Banner, id=banner_id)

    if request.method == 'POST':
        banner.delete()
        messages.success(request, 'Banner removido.')
        return redirect('admin_banners')

    return render(request, 'core/admin_banner_excluir.html', {'banner': banner})


# ═══════════════════════════════════════════════════════════
#  VACINAS — Guia de Vacinação
# ═══════════════════════════════════════════════════════════

def vacinas(request):
    caes = Vacina.objects.filter(ativo=True, especie__in=['cao', 'ambos'])
    gatos = Vacina.objects.filter(ativo=True, especie__in=['gato', 'ambos'])
    return render(request, 'core/vacinas.html', {'caes': caes, 'gatos': gatos})


@login_required
def admin_vacinas(request):
    if not request.user.is_staff:
        return redirect('index')
    vacinas = Vacina.objects.all()
    return render(request, 'core/admin_vacinas.html', {'vacinas': vacinas})


@login_required
def admin_vacina_adicionar(request):
    if not request.user.is_staff:
        return redirect('index')

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        idade = request.POST.get('idade_recomendada', '').strip()
        periodicidade = request.POST.get('periodicidade', '').strip()
        descricao = request.POST.get('descricao', '').strip()
        especie = request.POST.get('especie', 'ambos')
        ativo = request.POST.get('ativo') == 'on'

        if not nome or not idade:
            messages.error(request, 'Nome e idade recomendada são obrigatórios.')
        else:
            Vacina.objects.create(
                nome=nome,
                idade_recomendada=idade,
                periodicidade=periodicidade,
                descricao=descricao,
                especie=especie,
                ativo=ativo,
            )
            messages.success(request, f'Vacina "{nome}" cadastrada!')
            return redirect('admin_vacinas')

    return render(request, 'core/admin_vacina_form.html', {'acao': 'Adicionar'})


@login_required
def admin_vacina_editar(request, vacina_id):
    if not request.user.is_staff:
        return redirect('index')

    vacina = get_object_or_404(Vacina, id=vacina_id)

    if request.method == 'POST':
        vacina.nome = request.POST.get('nome', vacina.nome).strip()
        vacina.idade_recomendada = request.POST.get('idade_recomendada', vacina.idade_recomendada).strip()
        vacina.periodicidade = request.POST.get('periodicidade', vacina.periodicidade).strip()
        vacina.descricao = request.POST.get('descricao', vacina.descricao).strip()
        vacina.especie = request.POST.get('especie', vacina.especie)
        vacina.ativo = request.POST.get('ativo') == 'on'

        if not vacina.nome or not vacina.idade_recomendada:
            messages.error(request, 'Nome e idade recomendada são obrigatórios.')
        else:
            vacina.save()
            messages.success(request, f'Vacina "{vacina.nome}" atualizada!')
            return redirect('admin_vacinas')

    return render(request, 'core/admin_vacina_form.html', {'vacina': vacina, 'acao': 'Editar'})


@login_required
def admin_vacina_excluir(request, vacina_id):
    if not request.user.is_staff:
        return redirect('index')

    vacina = get_object_or_404(Vacina, id=vacina_id)

    if request.method == 'POST':
        vacina.delete()
        messages.success(request, 'Vacina removida.')
        return redirect('admin_vacinas')

    return render(request, 'core/admin_vacina_excluir.html', {'vacina': vacina})
