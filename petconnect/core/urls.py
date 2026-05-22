from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adotar/', views.listagem, name='listagem'),
    path('pet/<int:pet_id>/', views.detalhe, name='detalhe'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('painel/', views.painel_adotante, name='painel_adotante'),
    path('ong/solicitacoes/', views.solicitacoes_adocao, name='solicitacoes_adocao'),
    path('perfil/editar/', views.editar_usuario, name='editar_usuario'),
]
