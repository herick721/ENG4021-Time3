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

    # ── Informação / Estáticas ─────────────────────────────
    path('como-funciona/', views.como_funciona, name='como_funciona'),
    path('contato/', views.contato, name='contato'),
    path('pos-adocao/', views.pos_adocao, name='pos_adocao'),

    # ── Configurações ─────────────────────────────────────
    path('configuracoes/seguranca/', views.configuracoes_seguranca, name='configuracoes_seguranca'),
    path('configuracoes/excluir-conta/', views.excluir_conta, name='excluir_conta'),

    # ── ONG — Relatório ───────────────────────────────────
    path('ong/relatorio/', views.relatorio_ong, name='relatorio_ong'),

    # ── Parceiros ─────────────────────────────────────────
    path('parceiros/', views.parceiros, name='parceiros'),
    path('parceiros/admin/', views.admin_parceiros, name='admin_parceiros'),
    path('parceiros/admin/adicionar/', views.admin_parceiro_adicionar, name='admin_parceiro_adicionar'),
    path('parceiros/admin/editar/<int:parceiro_id>/', views.admin_parceiro_editar, name='admin_parceiro_editar'),
    path('parceiros/admin/excluir/<int:parceiro_id>/', views.admin_parceiro_excluir, name='admin_parceiro_excluir'),

    # ── Banners (Carrossel) ───────────────────────────────
    path('banners/admin/', views.admin_banners, name='admin_banners'),
    path('banners/admin/adicionar/', views.admin_banner_adicionar, name='admin_banner_adicionar'),
    path('banners/admin/editar/<int:banner_id>/', views.admin_banner_editar, name='admin_banner_editar'),
    path('banners/admin/excluir/<int:banner_id>/', views.admin_banner_excluir, name='admin_banner_excluir'),

    # ── Guia de Vacinação ─────────────────────────────────
    path('vacinas/', views.vacinas, name='vacinas'),
    path('vacinas/admin/', views.admin_vacinas, name='admin_vacinas'),
    path('vacinas/admin/adicionar/', views.admin_vacina_adicionar, name='admin_vacina_adicionar'),
    path('vacinas/admin/editar/<int:vacina_id>/', views.admin_vacina_editar, name='admin_vacina_editar'),
    path('vacinas/admin/excluir/<int:vacina_id>/', views.admin_vacina_excluir, name='admin_vacina_excluir'),
]
