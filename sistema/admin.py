from django.contrib import admin
from .models import Fornecedor, Pedido, DadosPedido, Produto, ClassificacaoProduto, Parametro

admin.site.register(Fornecedor)
admin.site.register(Pedido)
admin.site.register(DadosPedido)
admin.site.register(Produto)
admin.site.register(ClassificacaoProduto)
admin.site.register(Parametro)