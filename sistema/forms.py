from django import forms

from .models import Pedido, Fornecedor, ClassificacaoProduto

class FornecedorForm(forms.ModelForm):

    class Meta:
        model = Fornecedor
        fields = ('razao', 'cnpj',)
        
class PedidoForm(forms.ModelForm):

    class Meta:
        model = Pedido
        fields = ('fornecedor', 'numero', 'data', 'data_previsao', 'prazo', 'prazo_medio', 'desconto', 'loja', 'total', 'status', 'bonificacao', 'frete', 'observacao')

class ClassificacaoProdutoForm(forms.ModelForm):

    class Meta:
        model = ClassificacaoProduto
        fields = ('secao', 'sub_secao', 'estilo', 'formato', 'superior', 'abertura', 'membro', 'detalhe', 'material',)

    def __init__(self, *args, **kwargs):
        super(ClassificacaoProdutoForm, self).__init__(*args, **kwargs)
        self.fields['secao'].required = True
        self.fields['sub_secao'].required = False
        self.fields['estilo'].required = False
        self.fields['formato'].required = False
        self.fields['superior'].required = False
        self.fields['abertura'].required = False
        self.fields['membro'].required = False
        self.fields['detalhe'].required = False
        self.fields['material'].required = False