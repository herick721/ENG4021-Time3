from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Ong, Adotante, Pet, PetImage, SolicitacaoAdocao, Favorito, Parceiro, Banner, Vacina, Notificacao, Avaliacao


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'tipo', 'cidade', 'estado', 'is_active', 'date_joined')
    list_filter = ('tipo', 'is_active', 'estado')
    search_fields = ('username', 'email', 'cidade')
    fieldsets = UserAdmin.fieldsets + (
        ('PetConnect', {'fields': ('tipo', 'telefone', 'cidade', 'estado')}),
    )


@admin.register(Ong)
class OngAdmin(admin.ModelAdmin):
    list_display = ('nome_ong', 'usuario', 'cnpj', 'responsavel')
    search_fields = ('nome_ong', 'cnpj', 'responsavel')
    raw_id_fields = ('usuario',)


@admin.register(Adotante)
class AdotanteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_moradia', 'idade', 'ocupacao', 'moradores')
    list_filter = ('tipo_moradia',)
    search_fields = ('usuario__username', 'usuario__email')
    raw_id_fields = ('usuario',)


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especie', 'porte', 'sexo', 'idade_texto', 'status', 'ong', 'urgente')
    list_filter = ('especie', 'porte', 'sexo', 'status', 'urgente', 'vacinado', 'castrado')
    search_fields = ('nome', 'raca', 'descricao', 'ong__nome_ong')
    raw_id_fields = ('ong',)


@admin.register(SolicitacaoAdocao)
class SolicitacaoAdocaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'adotante', 'pet', 'status', 'data_solicitacao')
    list_filter = ('status', 'data_solicitacao')
    search_fields = ('adotante__usuario__username', 'pet__nome')
    raw_id_fields = ('adotante', 'pet')


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('adotante', 'pet', 'data_adicao')
    search_fields = ('adotante__usuario__username', 'pet__nome')
    raw_id_fields = ('adotante', 'pet')


@admin.register(Parceiro)
class ParceiroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'ativo', 'data_criacao')
    list_filter = ('tipo', 'ativo')
    search_fields = ('nome', 'descricao_curta')


@admin.register(PetImage)
class PetImageAdmin(admin.ModelAdmin):
    list_display = ('pet', 'ordem')
    list_filter = ('pet',)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ativo', 'ordem')
    list_filter = ('ativo',)


@admin.register(Vacina)
class VacinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especie', 'idade_recomendada', 'ativo')
    list_filter = ('especie', 'ativo')
    search_fields = ('nome',)


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'tipo', 'lida', 'data_criacao')
    list_filter = ('tipo', 'lida', 'data_criacao')
    search_fields = ('titulo', 'usuario__email')
    raw_id_fields = ('usuario',)


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('ong', 'adotante', 'nota', 'data_criacao')
    list_filter = ('nota', 'data_criacao')
    raw_id_fields = ('ong', 'adotante')
