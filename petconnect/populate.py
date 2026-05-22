import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'petconnect.settings')
django.setup()

from core.models import Usuario, Ong, Adotante, Pet, SolicitacaoAdocao, Favorito

def populate():
    # Limpa dados existentes
    Usuario.objects.all().delete()

    print("Criando usuários...")
    
    # Criando ONG
    u_ong = Usuario.objects.create_user(username='ong_patinhas', password='123', email='contato@patinhas.org',
                                        first_name='ONG', last_name='Patinhas', tipo='ong',
                                        cidade='São Paulo', estado='SP', telefone='(11) 99999-9999')
    ong = Ong.objects.create(usuario=u_ong, nome_ong='ONG Patinhas Felizes', responsavel='Maria')

    u_ong2 = Usuario.objects.create_user(username='ong_anjos', password='123', email='contato@anjos.org',
                                        first_name='ONG', last_name='Anjos', tipo='ong',
                                        cidade='Rio de Janeiro', estado='RJ', telefone='(21) 99999-9999')
    ong2 = Ong.objects.create(usuario=u_ong2, nome_ong='Anjos de Quatro Patas', responsavel='João')

    # Criando Adotante
    u_adotante = Usuario.objects.create_user(username='joaosilva', password='123', email='joao@email.com',
                                            first_name='João', last_name='Silva', tipo='adotante',
                                            cidade='São Paulo', estado='SP', telefone='(11) 98888-8888')
    adotante = Adotante.objects.create(usuario=u_adotante, tipo_moradia='house-yard', idade=30, ocupacao='Engenheiro', moradores='2 adultos')

    u_adotante2 = Usuario.objects.create_user(username='maria', password='123', email='maria@email.com',
                                            first_name='Maria', last_name='Oliveira', tipo='adotante',
                                            cidade='Rio de Janeiro', estado='RJ', telefone='(21) 97777-7777')
    adotante2 = Adotante.objects.create(usuario=u_adotante2, tipo_moradia='apt', idade=25, ocupacao='Professora', moradores='1 adulto')

    print("Criando pets...")
    
    pet1 = Pet.objects.create(ong=ong, nome='Bolinha', especie='cao', porte='medio', idade_texto='2 anos', sexo='macho',
                              raca='SRD', vacinado=True, castrado=True, amigo_criancas=True, amigo_outros_pets=False,
                              status='disponivel', imagem_emoji='🐶', cor_fundo='bg-pink', urgente=True, descricao='Bolinha é um cachorro alegre e cheio de energia que adora brincar ao ar livre. Convive bem com crianças e é muito carinhoso com seus tutores. Está em busca de uma família que possa dar muito amor e passeios diários. Ele é dócil, obediente e aprende comandos rapidamente. Adora petiscos e carinhos!')

    pet2 = Pet.objects.create(ong=ong2, nome='Mel', especie='gato', porte='pequeno', idade_texto='1 ano', sexo='femea',
                              raca='SRD', vacinado=True, castrado=False, amigo_criancas=True, amigo_outros_pets=True,
                              status='disponivel', imagem_emoji='🐈', cor_fundo='bg-peach', urgente=False, descricao='Gatinha muito meiga, gosta de dormir no sofá.')

    pet3 = Pet.objects.create(ong=ong, nome='Thor', especie='cao', porte='grande', idade_texto='4 anos', sexo='macho',
                              raca='Labrador', vacinado=True, castrado=True, amigo_criancas=True, amigo_outros_pets=True,
                              status='analise', imagem_emoji='🐕', cor_fundo='bg-blue', urgente=False, descricao='Cão grandão com coração de filhote. Adora água.')

    pet4 = Pet.objects.create(ong=ong2, nome='Nina', especie='gato', porte='pequeno', idade_texto='3 anos', sexo='femea',
                              raca='Persa', vacinado=True, castrado=True, amigo_criancas=False, amigo_outros_pets=False,
                              status='lar_temporario', imagem_emoji='🐱', cor_fundo='bg-purple', urgente=False, descricao='Gata mais reservada, ideal para ambientes tranquilos.')

    print("Criando solicitações e favoritos...")
    
    SolicitacaoAdocao.objects.create(adotante=adotante, pet=pet3, status='entrevista')
    SolicitacaoAdocao.objects.create(adotante=adotante2, pet=pet2, status='pendente')

    Favorito.objects.create(adotante=adotante, pet=pet1)
    Favorito.objects.create(adotante=adotante, pet=pet3)
    Favorito.objects.create(adotante=adotante2, pet=pet4)

    print("Banco de dados populado com sucesso!")

if __name__ == '__main__':
    populate()
