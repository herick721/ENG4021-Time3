from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    TIPO_CHOICES = (
        ('adotante', 'Adotante'),
        ('ong', 'ONG/Resgatador'),
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='adotante')
    telefone = models.CharField(max_length=20, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        return self.username

class Ong(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='ong_profile')
    nome_ong = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=20, blank=True, null=True)
    responsavel = models.CharField(max_length=100)
    sobre = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome_ong

class Adotante(models.Model):
    TIPO_MORADIA_CHOICES = (
        ('apt', 'Apartamento'),
        ('house-yard', 'Casa com quintal'),
        ('house', 'Casa sem quintal'),
        ('other', 'Outro'),
    )
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='adotante_profile')
    tipo_moradia = models.CharField(max_length=20, choices=TIPO_MORADIA_CHOICES, blank=True, null=True)
    idade = models.IntegerField(blank=True, null=True)
    ocupacao = models.CharField(max_length=100, blank=True, null=True)
    moradores = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username

class Pet(models.Model):
    ESPECIE_CHOICES = (
        ('cao', 'Cão'),
        ('gato', 'Gato'),
        ('outro', 'Outro'),
    )
    PORTE_CHOICES = (
        ('pequeno', 'Pequeno'),
        ('medio', 'Médio'),
        ('grande', 'Grande'),
    )
    SEXO_CHOICES = (
        ('macho', 'Macho'),
        ('femea', 'Fêmea'),
    )
    STATUS_CHOICES = (
        ('disponivel', 'Disponível'),
        ('analise', 'Em análise'),
        ('lar_temporario', 'Lar temporário'),
        ('adotado', 'Adotado'),
    )

    ong = models.ForeignKey(Ong, on_delete=models.CASCADE, related_name='pets')
    nome = models.CharField(max_length=100)
    especie = models.CharField(max_length=10, choices=ESPECIE_CHOICES)
    porte = models.CharField(max_length=20, choices=PORTE_CHOICES)
    idade_texto = models.CharField(max_length=50, help_text="Ex: 2 anos, 6 meses")
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    raca = models.CharField(max_length=100, default='SRD')
    descricao = models.TextField(blank=True, null=True)
    
    # Saúde
    vacinado = models.BooleanField(default=False)
    castrado = models.BooleanField(default=False)
    vermifugado = models.BooleanField(default=False)
    microchip = models.BooleanField(default=False)
    
    # Comportamento
    amigo_criancas = models.BooleanField(default=False)
    amigo_outros_pets = models.BooleanField(default=False)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponivel')
    
    # Detalhes visuais baseados no HTML
    imagem_emoji = models.CharField(max_length=10, default='🐶')
    cor_fundo = models.CharField(max_length=20, default='bg-pink', help_text="Classe CSS de cor. Ex: bg-pink, bg-peach, bg-blue, etc")
    urgente = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} ({self.get_especie_display()})"

class SolicitacaoAdocao(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('entrevista', 'Em Entrevista'),
        ('aprovada', 'Aprovada'),
        ('recusada', 'Recusada'),
        ('concluida', 'Concluída'),
    )
    adotante = models.ForeignKey(Adotante, on_delete=models.CASCADE, related_name='solicitacoes')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='solicitacoes')
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    motivo_recusa = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Solicitação de {self.adotante.usuario.username} para {self.pet.nome}"

class Favorito(models.Model):
    adotante = models.ForeignKey(Adotante, on_delete=models.CASCADE, related_name='favoritos')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='favoritados')
    data_adicao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('adotante', 'pet')

    def __str__(self):
        return f"{self.adotante.usuario.username} favoritou {self.pet.nome}"
