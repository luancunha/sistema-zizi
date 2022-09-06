from django.db import models

class Fornecedor(models.Model):
    razao = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=50)
    
    def __str__(self):
        return self.razao

class Pedido(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    numero = models.CharField(max_length=20)
    data = models.DateField()
    data_previsao = models.DateField()
    prazo = models.CharField(max_length=30)
    prazo_medio = models.IntegerField()
    desconto = models.DecimalField(max_digits=4, decimal_places=2)
    loja = models.CharField(max_length=2)
    total = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(max_length=2)
    bonificacao = models.DecimalField(max_digits=6, decimal_places=2)
    frete = models.DecimalField(max_digits=6, decimal_places=2)
    observacao = models.TextField(default=None, blank=True, null=True)
    
    def __str__(self):
        return str(self.numero)

class DadosPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    marca = models.CharField(max_length=50)
    produto = models.CharField(max_length=50)
    ref = models.CharField(max_length=20)
    tamanho = models.CharField(max_length=20)
    quant = models.IntegerField()
    quant_baixa = models.IntegerField()
    custo = models.DecimalField(max_digits=7, decimal_places=2)
    icms = models.DecimalField(max_digits=4, decimal_places=2)
    status = models.BooleanField(default=False)
    status_class = models.BooleanField(default=False)
    preco_venda = models.DecimalField(max_digits=7, decimal_places=2)
    
    def __str__(self):
        return str(self.id)

class Produto(models.Model):
    mar_pro_ref = models.JSONField(unique=True)
    
    def __str__(self):
        return str(self.id)

class ClassificacaoProduto(models.Model):
    SECAO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('Q', 'Quarto'),
        ('S', 'Sala'),
        ('CO', 'Copa'),
        ('B', 'Banheiro'),
        ('CZ', 'Cozinha'),
        ('U', 'Unissex'),
    ]
    SUB_SECAO_CHOICES = [
        ('A', 'Adulto'),
        ('J', 'Juvenil'),
        ('I', 'Infantil'),
        ('C', 'Casal'),
        ('S', 'Solteiro'),
        ('BE', 'Berco'),
        ('BB', 'Bebe'),
    ]
    ESTILO_CHOICES = [
        ('C', 'Casual'),
        ('S', 'Social'),
        ('EF', 'Esporte Fino'),
        ('ES', 'Esportivo'),
        ('P', 'Praia'),
    ]
    FORMATO_CHOICES = [
        ('A', 'Ampla'),
        ('T', 'Tradicional'),
        ('F', 'Fina'),
        ('G', 'Gestante'),
        ('Q', 'Quadrada'),
        ('RE', 'Redonda'),
        ('RT', 'Retangular'),
        ('O', 'Oval'),
    ]
    SUPERIOR_CHOICES = [
        ('B', 'Baixa'),
        ('I', 'Intemediaria'),
        ('A', 'Alta'),
        ('E', 'Extra-alta'),
    ]
    ABERTURA_CHOICES = [
        ('AB', 'Aberta'),
        ('MA', 'Meia aberta'),
        ('F', 'Fechada'),
        ('D', 'Decote'),
        ('P', 'Polo'),
        ('V', 'V'),
        ('AM', 'Amamentacao'),
    ]
    MEMBRO_CHOICES = [
        ('A', 'Alca'),
        ('MI', 'Mini'),
        ('C', 'Curta'),
        ('ME', 'Media'),
        ('3', '3/4'),
        ('L', 'Longa'),
    ]
    DETALHE_CHOICES = [
        ('BS', 'Bolso'),
        ('CG', 'Cargo'),
        ('CP', 'Capuz'),
        ('BJ', 'Bojo'),
        ('I', 'Inverno'),
    ]
    MATERIAL_CHOICES = [
        ('A', 'Algodao'),
        ('B', 'Brim'),
        ('J', 'Jeans'),
        ('MA', 'Malha'),
        ('MI', 'Moletin'),
        ('MO', 'Moleton'),
        ('SA', 'Sarja'),
        ('SI', 'Sintetico'),
    ]
    prod = models.ForeignKey(Produto, on_delete=models.CASCADE)
    secao = models.CharField(max_length=2, choices=SECAO_CHOICES, null=True)
    sub_secao = models.CharField(max_length=2, choices=SUB_SECAO_CHOICES, null=True)
    estilo = models.CharField(max_length=2, choices=ESTILO_CHOICES, null=True)
    formato = models.CharField(max_length=2, choices=FORMATO_CHOICES, null=True)
    superior = models.CharField(max_length=1, choices=SUPERIOR_CHOICES, null=True)
    abertura = models.CharField(max_length=2, choices=ABERTURA_CHOICES, null=True)
    membro = models.CharField(max_length=2, choices=MEMBRO_CHOICES, null=True)
    detalhe = models.CharField(max_length=2, choices=DETALHE_CHOICES, null=True)
    material = models.CharField(max_length=2, choices=MATERIAL_CHOICES, null=True)
    
    def __str__(self):
        return str(self.id)

class Parametro(models.Model):
    markup = models.DecimalField(max_digits=6, decimal_places=2)
    icms_minas = models.DecimalField(max_digits=6, decimal_places=2)
    icms_fora = models.DecimalField(max_digits=6, decimal_places=2)
    icms_importado = models.DecimalField(max_digits=6, decimal_places=2)
    taxa = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return str(self.id)