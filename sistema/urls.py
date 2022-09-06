from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('pedido/', views.pedido, name='pedido'),
    path('pedido/novo/', views.ped_novo, name='ped_novo'),
    path('pedido/edita/<int:pk>', views.ped_edita, name='ped_edita'),
    path('pedido/deleta/<int:pk>', views.ped_deleta, name='ped_deleta'),

    path('pedido/copia/<int:pk>', views.copiar_pedido, name='copiar_pedido'),
    
    path('pedido/<int:pk>/dados', views.ped_dados, name='ped_dados'),
    path('pedido/<int:pkp>/dados/deleta/<int:pkd>', views.ped_dados_deleta, name='ped_dados_deleta'),

    path('fornecedor/', views.fornecedor, name='fornecedor'),
    path('fornecedor/novo/', views.forn_novo, name='forn_novo'),
    path('fornecedor/edita/<int:pk>', views.forn_edita, name='forn_edita'),
    path('fornecedor/deleta/<int:pk>', views.forn_deleta, name='forn_deleta'),

    path('relatorio/', views.relatorio, name='relatorio'),

    path('classificacao/<int:pkd>', views.classificacao, name='classificacao'),

    path('pedido/<int:pk>/imprimir/', views.imprimir, name='imprimir'),

    path('pedido/dados/baixa/', views.baixa, name='baixa'),
    path('pedido/<int:pk>/baixa_todo/', views.baixar_todo_pedido, name='baixar_todo_pedido'),
]