from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Ong, Adotante, Pet, SolicitacaoAdocao, Favorito


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
