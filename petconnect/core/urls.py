from django.urls import path
from . import views

urlpatterns = [
    # ── Públicas ──────────────────────────────────────────
    path('', views.index, name='index'),
    path('adotar/', views.listagem, name='listagem'),
    path('adotar/filtros/', views.listagem_filtros, name='listagem_filtros'),
    path('adotar/busca/', views.busca_avancada, name='busca_avancada'),
    path('pet/<int:pet_id>/', views.detalhe, name='detalhe'),
    path('ong/<int:ong_id>/', views.pagina_ong, name='pagina_ong'),
    path('recuperar-senha/', views.recuperar_senha, name='recuperar_senha'),

    # ── Autenticação ──────────────────────────────────────
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),

    # ── Qualquer usuário logado ───────────────────────────
    path('perfil/editar/', views.editar_usuario, name='editar_usuario'),
    path('notificacoes/', views.notificacoes, name='notificacoes'),
    path('onboarding/', views.onboarding, name='onboarding'),

    # ── Adotante ──────────────────────────────────────────
    path('painel/', views.painel_adotante, name='painel_adotante'),
    path('painel/favoritos/', views.favoritos, name='favoritos'),
    path('painel/perfil/', views.perfil_adotante, name='perfil_adotante'),
    path('painel/historico/', views.historico_adocoes, name='historico_adocoes'),
    path('pet/<int:pet_id>/solicitar/', views.confirmacao_adocao, name='confirmacao_adocao'),
    path('pet/<int:pet_id>/favoritar/', views.toggle_favorito, name='toggle_favorito'),
    path('pet/<int:pet_id>/termo/', views.termo_adocao, name='termo_adocao'),
    path('ong/<int:ong_id>/avaliar/', views.avaliar_ong, name='avaliar_ong'),
    path('ong/<int:ong_id>/chat/', views.chat_ong, name='chat_ong'),

    # ── ONG ───────────────────────────────────────────────
    path('ong/dashboard/', views.dashboard_ong, name='dashboard_ong'),
    path('ong/solicitacoes/', views.solicitacoes_adocao, name='solicitacoes_adocao'),
    path('ong/solicitacao/<int:sol_id>/atualizar/', views.atualizar_solicitacao, name='atualizar_solicitacao'),
    path('ong/cadastrar-pet/', views.cadastro_pet, name='cadastro_pet'),
    path('pet/<int:pet_id>/editar/', views.editar_pet, name='editar_pet'),
    path('pet/<int:pet_id>/excluir/', views.excluir_pet, name='excluir_pet'),
    path('ong/lar-temporario/', views.lar_temporario, name='lar_temporario'),
    path('ong/cadastro-ong/', views.cadastro_ong, name='cadastro_ong'),
]
