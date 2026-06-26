import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'petconnect.settings')
django.setup()

from core.models import Usuario, Ong, Adotante, Pet, PetImage, SolicitacaoAdocao, Favorito, Notificacao, Avaliacao
from datetime import datetime, timedelta
from django.utils import timezone


def populate():
    # Limpa dados existentes
    Usuario.objects.all().delete()
    PetImage.objects.all().delete()

    print("Criando usuários...")

    # ═══════════════════════════════════
    #  ONGs
    # ═══════════════════════════════════

    u_ong1 = Usuario.objects.create_user(
        username='ong_patinhas', password='123', email='contato@patinhas.org',
        first_name='ONG', last_name='Patinhas', tipo='ong',
        cidade='São Paulo', estado='SP', telefone='(11) 99999-9999',
        date_joined=timezone.make_aware(datetime(2018, 3, 10))
    )
    ong1 = Ong.objects.create(
        usuario=u_ong1, nome_ong='ONG Patinhas Felizes', responsavel='Maria Santos',
        cnpj='12.345.678/0001-90'
    )

    u_ong2 = Usuario.objects.create_user(
        username='ong_anjos', password='123', email='contato@anjos.org',
        first_name='ONG', last_name='Anjos', tipo='ong',
        cidade='Rio de Janeiro', estado='RJ', telefone='(21) 99999-9999',
        date_joined=timezone.make_aware(datetime(2020, 7, 22))
    )
    ong2 = Ong.objects.create(
        usuario=u_ong2, nome_ong='Anjos de Quatro Patas', responsavel='João Oliveira',
        cnpj='23.456.789/0001-01'
    )

    u_ong3 = Usuario.objects.create_user(
        username='ong_resgate', password='123', email='contato@resgateanimal.org',
        first_name='ONG', last_name='Resgate', tipo='ong',
        cidade='Belo Horizonte', estado='MG', telefone='(31) 98888-8888',
        date_joined=timezone.make_aware(datetime(2021, 11, 5))
    )
    ong3 = Ong.objects.create(
        usuario=u_ong3, nome_ong='Instituto Resgate Animal', responsavel='Ana Costa',
        cnpj='34.567.890/0001-12'
    )

    u_ong4 = Usuario.objects.create_user(
        username='ong_bicho', password='123', email='contato@bichoamado.org',
        first_name='ONG', last_name='Bicho', tipo='ong',
        cidade='Curitiba', estado='PR', telefone='(41) 97777-7777',
        date_joined=timezone.make_aware(datetime(2019, 1, 15))
    )
    ong4 = Ong.objects.create(
        usuario=u_ong4, nome_ong='Bicho Amado', responsavel='Carlos Pereira',
        cnpj='45.678.901/0001-23'
    )

    # ═══════════════════════════════════
    #  Adotantes
    # ═══════════════════════════════════

    u_ad1 = Usuario.objects.create_user(
        username='joaosilva', password='123', email='joao@email.com',
        first_name='João', last_name='Silva', tipo='adotante',
        cidade='São Paulo', estado='SP', telefone='(11) 98888-8888'
    )
    ad1 = Adotante.objects.create(usuario=u_ad1, tipo_moradia='house-yard', idade=30, ocupacao='Engenheiro Civil', moradores='2 adultos, 1 criança')

    u_ad2 = Usuario.objects.create_user(
        username='mariaoliveira', password='123', email='maria@email.com',
        first_name='Maria', last_name='Oliveira', tipo='adotante',
        cidade='Rio de Janeiro', estado='RJ', telefone='(21) 97777-7777'
    )
    ad2 = Adotante.objects.create(usuario=u_ad2, tipo_moradia='apt', idade=25, ocupacao='Professora', moradores='1 adulto')

    u_ad3 = Usuario.objects.create_user(
        username='pedrosantos', password='123', email='pedro@email.com',
        first_name='Pedro', last_name='Santos', tipo='adotante',
        cidade='Belo Horizonte', estado='MG', telefone='(31) 96666-6666'
    )
    ad3 = Adotante.objects.create(usuario=u_ad3, tipo_moradia='house', idade=42, ocupacao='Médico Veterinário', moradores='2 adultos, 2 crianças')

    u_ad4 = Usuario.objects.create_user(
        username='anacarla', password='123', email='ana@email.com',
        first_name='Ana', last_name='Carla', tipo='adotante',
        cidade='Curitiba', estado='PR', telefone='(41) 95555-5555'
    )
    ad4 = Adotante.objects.create(usuario=u_ad4, tipo_moradia='apt', idade=28, ocupacao='Arquiteta', moradores='1 adulto, 1 gato')

    u_ad5 = Usuario.objects.create_user(
        username='lucas_lima', password='123', email='lucas@email.com',
        first_name='Lucas', last_name='Lima', tipo='adotante',
        cidade='São Paulo', estado='SP', telefone='(11) 94444-4444'
    )
    ad5 = Adotante.objects.create(usuario=u_ad5, tipo_moradia='house-yard', idade=35, ocupacao='Advogado', moradores='2 adultos')

    print("Criando pets...")
    hoje = timezone.now()

    pets_data = [
        # ONG 1 - Patinhas Felizes (SP)
        {'ong': ong1, 'nome': 'Bolinha', 'especie': 'cao', 'porte': 'medio', 'idade': '2 anos', 'sexo': 'macho',
         'raca': 'SRD', 'vacinado': True, 'castrado': True, 'amigo_criancas': True, 'amigo_outros_pets': False,
         'status': 'disponivel', 'emoji': '🐶', 'cor': 'bg-pink', 'urgente': True,
         'desc': 'Bolinha é um cachorro alegre e cheio de energia que adora brincar ao ar livre. Convive bem com crianças e é muito carinhoso. Adora petiscos e carinhos!'},
        {'ong': ong1, 'nome': 'Luna', 'especie': 'gato', 'porte': 'pequeno', 'idade': '1 ano', 'sexo': 'femea',
         'raca': 'SRD', 'vacinado': True, 'castrado': True, 'amigo_criancas': True, 'amigo_outros_pets': True,
         'status': 'disponivel', 'emoji': '🐱', 'cor': 'bg-peach', 'urgente': False,
         'desc': 'Luna é uma gatinha doce e brincalhona. Ama um colo e ronrona sem parar. Ideal para apartamento.'},
        {'ong': ong1, 'nome': 'Thor', 'especie': 'cao', 'porte': 'grande', 'idade': '4 anos', 'sexo': 'macho',
         'raca': 'Labrador', 'vacinado': True, 'castrado': True, 'amigo_criancas': True, 'amigo_outros_pets': True,
         'status': 'adotado', 'emoji': '🐕', 'cor': 'bg-blue', 'urgente': False,
         'desc': 'Cão grandão com coração de filhote. Adora água e brincar no parque. Já foi adotado! 😊'},
        {'ong': ong1, 'nome': 'Pipoca', 'especie': 'cao', 'porte': 'pequeno', 'idade': '6 meses', 'sexo': 'femea',
         'raca': 'SRD', 'vacinado': True, 'castrado': False, 'amigo_criancas': True, 'amigo_outros_pets': True,
         'status': 'disponivel', 'emoji': '🐶', 'cor': 'bg-purple', 'urgente': True,
         'desc': 'Filhotinha encontrada na chuva. É brincalhona, esperta e já sabe fazer as necessidades no jornal. Vacinas em dia.'},
        {'ong': ong1, 'nome': 'Freddy', 'especie': 'gato', 'porte': 'medio', 'idade': '3 anos', 'sexo': 'macho',
         'raca': 'Laranja SRD', 'vacinado': True, 'castrado': True, 'amigo_criancas': False, 'amigo_outros_pets': True,
         'status': 'disponivel', 'emoji': '🐈', 'cor': 'bg-orange', 'urgente': False,
         'desc': 'Gato laranja carinhoso, mas prefere ambientes tranquilos sem crianças pequenas. Companheiro pra vida.'},

        # ONG 2 - Anjos de Quatro Patas (RJ)
        {'ong': ong2, 'nome': 'Mel', 'especie': 'gato', 'porte': 'pequeno', 'idade': '1 ano', 'sexo': 'femea',
         'raca': 'SRD', 'vacinado': True, 'castrado': False, 'amigo_criancas': True, 'amigo_outros_pets': True,
         'status': 'disponivel', 'emoji': '🐈', 'cor': 'bg-peach', 'urgente': False,
         'desc': 'Gatinha muito meiga e carente. Gosta de dormir no sofá e tomar sol na janela.'},
        {'ong': ong2, 'nome': 'Nina', 'especie': 'gato', 'porte': 'pequeno', 'idade': '3 anos', 'sexo': 'femea',
         'raca': 'Persa', 'vacinado': True, 'castrado': True, 'amigo_criancas': False, 'amigo_outros_pets': False,
         'status': 'lar_temporario', 'emoji': '🐱', 'cor': 'bg-purple', 'urgente': False,
         'desc': 'Gata mais reservada, ideal para ambientes tranquilos sem outros animais.'},
        {'ong': ong2, 'nome': 'Buddy', 'especie': 'cao', 'porte': 'medio', 'idade': '2 anos', 'sexo': 'macho',
         'raca': 'Golden Retriever', 'vacinado': True, 'castrado': True, 'amigo_criancas': True, 'amigo_outros_pets': True,
         'status': 'disponivel', 'emoji': '🐶', 'cor': 'bg-gold', 'urgente': False,
         'desc': 'Buddy é o cachorro mais amigável que você vai conhecer. Ideal para famílias com crianças.'},
        {'ong': ong2, 'nome': 'Pretinha', 'especie': 'cao', 'porte': 'medio', 'idade': '5 anos', 'sexo': 'femea',
         'raca': 'SRD', 'vacinado': True, 'castrado': True, 'amigo_criancas': True, 'amigo_outros_pets': True,
         'status': 'disponivel', 'emoji': '🐕‍🦺', 'cor': 'bg-dark', 'urgente': False,
         'desc': 'Pretinha foi resgatada de maus-tratos e hoje é uma cadela dócil e grata. Dá amor incondicional.'},

        # ONG 3 - Instituto Resgate Animal (MG)
        {'ong': ong3, 'nome': 'Max', 'especie': 'cao', 'porte': 'grande', 'idade': '3 anos', 'sexo': 'macho',
         'raca': 'Pastor Alemão', 'vacinado': True, 'castrado': True, 'amigo_criancas': True, 'amigo_outros_pets': False,
         'status': 'disponivel', 'emoji': '🐕', 'cor': 'bg-brown', 'urgente': False,
         'desc': 'Max é um cão imponente mas de coração mole. Protetor e leal, precisa de espaço e dedicação.'},
        {'ong': ong3, 'nome': 'Mimi', 'especie': 'gato', 'porte': 'pequeno', 'idade': '8 meses', 'sexo': 'femea',
         'raca': 'SRD', 'vacinado': False, 'castrado': False, 'amigo_criancas': True, 'amigo_outros_pets': True,
         'status': 'disponivel', 'emoji': '🐱', 'cor': 'bg-white', 'urgente': True,
         'desc': 'Mimi precisa de vacinas e castração, mas é uma gatinha saudável e muito elétrica. Brinca com tudo!'},
        {'ong': ong3, 'nome': 'Rex', 'especie': 'cao', 'porte': 'medio', 'idade': '6 anos', 'sexo': 'macho',
         'raca': 'SRD', 'vacinado': True, 'castrado': True, 'amigo_criancas': False, 'amigo_outros_pets': True,
         'status': 'disponivel', 'emoji': '🐶', 'cor': 'bg-gray', 'urgente': False,
         'desc': 'Rex é um senhorzinho de 6 anos que merece um lar tranquilo para passar seus dias com amor e conforto.'},
        {'ong': ong3, 'nome': 'Amora', 'especie': 'cao', 'porte': 'pequeno', 'idade': '1 ano', 'sexo': 'femea',
         'raca': 'SRD', 'vacinado': True, 'castrado': True, 'amigo_criancas': True, 'amigo_outros_pets': True,
         'status': 'disponivel', 'emoji': '🐕', 'cor': 'bg-pink', 'urgente': False,
         'desc': 'Amora é uma cadela de porte pequeno cheia de energia. Ideal para quem busca uma companhia para corridas e passeios.'},

        # ONG 4 - Bicho Amado (PR)
        {'ong': ong4, 'nome': 'Tobias', 'especie': 'gato', 'porte': 'grande', 'idade': '4 anos', 'sexo': 'macho',
         'raca': 'Maine Coon', 'vacinado': True, 'castrado': True, 'amigo_criancas': True, 'amigo_outros_pets': False,
         'status': 'disponivel', 'emoji': '🐈', 'cor': 'bg-blue', 'urgente': False,
         'desc': 'Tobias é um gato grande e imponente de 4 anos. Muito carinhoso com seus humanos, mas prefere ser filho único.'},
        {'ong': ong4, 'nome': 'Cacau', 'especie': 'cao', 'porte': 'pequeno', 'idade': '2 anos', 'sexo': 'macho',
         'raca': 'SRD', 'vacinado': True, 'castrado': True, 'amigo_criancas': True, 'amigo_outros_pets': True,
         'status': 'disponivel', 'emoji': '🐶', 'cor': 'bg-brown', 'urgente': False,
         'desc': 'Cacau é um cãozinho de porte pequeno, muito amigável e sociável. Se dá bem com todos.'},
    ]

    pets = []
    for p in pets_data:
        pet = Pet.objects.create(
            ong=p['ong'], nome=p['nome'], especie=p['especie'], porte=p['porte'],
            idade_texto=p['idade'], sexo=p['sexo'], raca=p['raca'],
            vacinado=p['vacinado'], castrado=p['castrado'],
            amigo_criancas=p['amigo_criancas'], amigo_outros_pets=p['amigo_outros_pets'],
            status=p['status'], imagem_emoji=p['emoji'], cor_fundo=p['cor'],
            urgente=p['urgente'], descricao=p['desc']
        )
        pets.append(pet)

    print(f"  {len(pets)} pets criados!")

    print("Criando solicitações de adoção...")

    # Thor foi adotado
    SolicitacaoAdocao.objects.create(
        adotante=ad1, pet=pets[2], status='concluida',
        data_solicitacao=hoje - timedelta(days=45)
    )
    # Bolinha em processo
    s1 = SolicitacaoAdocao.objects.create(
        adotante=ad1, pet=pets[0], status='entrevista',
        data_solicitacao=hoje - timedelta(days=5)
    )
    # Mel pendente
    SolicitacaoAdocao.objects.create(
        adotante=ad2, pet=pets[5], status='pendente',
        data_solicitacao=hoje - timedelta(days=2)
    )
    # Buddy - concluida
    SolicitacaoAdocao.objects.create(
        adotante=ad3, pet=pets[7], status='concluida',
        data_solicitacao=hoje - timedelta(days=60)
    )
    # Max - em andamento
    SolicitacaoAdocao.objects.create(
        adotante=ad4, pet=pets[9], status='aprovada',
        data_solicitacao=hoje - timedelta(days=10)
    )
    # Amora - recusada
    SolicitacaoAdocao.objects.create(
        adotante=ad5, pet=pets[12], status='recusada',
        data_solicitacao=hoje - timedelta(days=20)
    )
    # Cacau - pendente para ad2
    SolicitacaoAdocao.objects.create(
        adotante=ad2, pet=pets[14], status='pendente',
        data_solicitacao=hoje - timedelta(hours=6)
    )
    # Pretinha - concluida
    SolicitacaoAdocao.objects.create(
        adotante=ad5, pet=pets[8], status='concluida',
        data_solicitacao=hoje - timedelta(days=90)
    )

    print("Criando favoritos...")
    Favorito.objects.create(adotante=ad1, pet=pets[0])   # Bolinha
    Favorito.objects.create(adotante=ad1, pet=pets[9])   # Max
    Favorito.objects.create(adotante=ad2, pet=pets[6])   # Nina (lar temporario)
    Favorito.objects.create(adotante=ad2, pet=pets[5])   # Mel
    Favorito.objects.create(adotante=ad3, pet=pets[10])  # Mimi
    Favorito.objects.create(adotante=ad3, pet=pets[4])   # Freddy
    Favorito.objects.create(adotante=ad4, pet=pets[8])   # Pretinha
    Favorito.objects.create(adotante=ad4, pet=pets[13])  # Tobias

    print("Criando notificações...")
    Notificacao.objects.create(usuario=u_ad1, tipo='success', titulo='Adoção concluída! 🎉',
                               mensagem='Parabéns! A adoção do Thor foi concluída com sucesso.', lida=True,
                               data_criacao=hoje - timedelta(days=44))
    Notificacao.objects.create(usuario=u_ad1, tipo='info', titulo='Entrevista agendada',
                               mensagem='A ONG Patinhas Felizes agendou uma entrevista para o Bolinha.', lida=False,
                               data_criacao=hoje - timedelta(days=3))
    Notificacao.objects.create(usuario=u_ad2, tipo='warning', titulo='Solicitação pendente',
                               mensagem='Sua solicitação para adotar a Mel está em análise.', lida=False,
                               data_criacao=hoje - timedelta(days=1))
    Notificacao.objects.create(usuario=u_ong1, tipo='info', titulo='Nova solicitação de adoção',
                               mensagem='João Silva quer adotar o Bolinha!', lida=False,
                               data_criacao=hoje - timedelta(days=5))
    Notificacao.objects.create(usuario=u_ong4, tipo='info', titulo='Nova solicitação de adoção',
                               mensagem='Maria Oliveira quer adotar o Cacau!', lida=False,
                               data_criacao=hoje - timedelta(hours=6))
    Notificacao.objects.create(usuario=u_ad5, tipo='danger', titulo='Solicitação recusada',
                               mensagem='Infelizmente sua solicitação para adotar a Amora foi recusada.', lida=True,
                               data_criacao=hoje - timedelta(days=18))

    print("Criando avaliações...")
    Avaliacao.objects.create(ong=ong1, adotante=ad1, nota=5, comentario='ONG maravilhosa! Todo o processo foi muito transparente.')
    Avaliacao.objects.create(ong=ong2, adotante=ad3, nota=5, comentario='Adotei o Buddy e foi a melhor decisão. A ONG dá todo o suporte.')
    Avaliacao.objects.create(ong=ong3, adotante=ad5, nota=4, comentario='Equipe muito dedicada. O processo de adoção foi rápido e bem organizado.')
    Avaliacao.objects.create(ong=ong1, adotante=ad2, nota=5, comentario='A Patinhas Felizes é referência em adoção responsável. Super recomendo!')
    Avaliacao.objects.create(ong=ong4, adotante=ad4, nota=4, comentario='Ótima ONG, mas gostaria que tivessem mais opções de gatos para adoção.')
    Avaliacao.objects.create(ong=ong2, adotante=ad1, nota=5, comentario='Adotei o Thor por meio deles e foi uma experiência incrível.')

    print("✅ Banco de dados populado com sucesso!")
    print(f"   {Usuario.objects.count()} usuários")
    print(f"   {Ong.objects.count()} ONGs")
    print(f"   {Adotante.objects.count()} adotantes")
    print(f"   {Pet.objects.count()} pets")
    print(f"   {SolicitacaoAdocao.objects.count()} solicitações")
    print(f"   {Favorito.objects.count()} favoritos")
    print(f"   {Notificacao.objects.count()} notificações")
    print(f"   {Avaliacao.objects.count()} avaliações")


if __name__ == '__main__':
    populate()
