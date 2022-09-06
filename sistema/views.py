from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Parametro, Pedido, DadosPedido, Fornecedor, Produto, ClassificacaoProduto
from .forms import PedidoForm, FornecedorForm, ClassificacaoProdutoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as login_as, logout as logout_as
from django.forms import modelformset_factory
from django.db.models import Avg, Count, Min, Sum
from random import randrange
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.db import connection, connections

def inicio(request):
    db_conn = connections['default']
    try:
        c = db_conn.cursor()
    except Exception as e:
        connected = False
    else:
        connected = True
    return render(request, 'inicio.html', {'connected':connected})

@login_required(login_url='/login/')
def pedido(request):
    query_set = Group.objects.filter(user = request.user)

    for g in query_set:
        loja_user = g.name

    if query_set.exists():
        if 'q' in request.GET and request.GET.get('q') != '':
            q = request.GET['q']
            if request.GET.get('tipo') is None:
                tipo = ''
            else:
                tipo = request.GET['tipo']
            data_ini = request.GET['data_ini']
            data_fim = request.GET['data_fim']
            if tipo == 'num':
                pedidos_lista = Pedido.objects.filter(numero=q).filter(loja=loja_user).filter(data__range=[data_ini, data_fim])
            elif tipo == 'forn':
                q = Fornecedor.objects.get(razao__contains=q)
                pedidos_lista = Pedido.objects.filter(fornecedor=q).filter(loja=loja_user).filter(data__range=[data_ini, data_fim])
            else:
                pedidos_lista = Pedido.objects.filter(loja=loja_user).order_by('-data')
        else:
            pedidos_lista = Pedido.objects.filter(loja=loja_user).order_by('-data')
    else:
        if 'q' in request.GET and request.GET.get('q') != '':
            q = request.GET['q']
            if request.GET.get('tipo') is None:
                tipo = ''
            else:
                tipo = request.GET['tipo']
            data_ini = request.GET['data_ini']
            data_fim = request.GET['data_fim']
            loja = request.GET['loja']
            if tipo == 'num':
                if loja != '00':
                    pedidos_lista = Pedido.objects.filter(numero=q).filter(loja=loja).filter(data__range=[data_ini, data_fim])
                else:
                    pedidos_lista = Pedido.objects.filter(numero=q).filter(data__range=[data_ini, data_fim])
            elif tipo == 'forn':
                if loja != '00':
                    q = Fornecedor.objects.get(razao__contains=q)
                    pedidos_lista = Pedido.objects.filter(fornecedor=q).filter(loja=loja).filter(data__range=[data_ini, data_fim])
                else:
                    q = Fornecedor.objects.get(razao__contains=q)
                    pedidos_lista = Pedido.objects.filter(fornecedor=q).filter(data__range=[data_ini, data_fim])
            else:
                pedidos_lista = Pedido.objects.all().order_by('-data')
        else:
            if 'loja' in request.GET:
                loja = request.GET['loja']
                if loja != '00':
                    pedidos_lista = Pedido.objects.all().filter(loja=loja).order_by('-data')
                else:
                    pedidos_lista = Pedido.objects.all().order_by('-data')
            else:
                pedidos_lista = Pedido.objects.all().order_by('-data')
    
    fornecedores = Fornecedor.objects.all()
    
    page = request.GET.get('page', 1)
    paginator = Paginator(pedidos_lista, 50)
    try:
        pedidos = paginator.page(page)
    except PageNotAnInteger:
        pedidos = paginator.page(1)
    except EmptyPage:
        pedidos = paginator.page(paginator.num_pages)
    
    return render(request, 'pedido.html', {'fornecedores': fornecedores, 'pedidos': pedidos, 'pedidos_lista': pedidos_lista})

@login_required(login_url='/login/')
def ped_novo(request):
    if request.method == "POST":
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.fornecedor = form.cleaned_data['fornecedor']
            pedido.numero = form.cleaned_data['numero']
            pedido.data = form.cleaned_data['data']
            pedido.data_previsao = form.cleaned_data['data_previsao']
            pedido.prazo = form.cleaned_data['prazo']
            pedido.prazo_medio = form.cleaned_data['prazo_medio']
            pedido.loja = form.cleaned_data['loja']
            pedido.total = form.cleaned_data['total']
            pedido.bonificacao = form.cleaned_data['bonificacao']
            pedido.frete = form.cleaned_data['frete']
            pedido.observacao = form.cleaned_data['observacao']

            pedido.save()
            messages.success(request, 'Pedido cadastrado com sucesso!')
            return redirect('pedido')
    else:
        form = PedidoForm()
    return render(request, 'pedido.html', {'form': form})

@login_required(login_url='/login/')
def ped_edita(request, pk):
    fornecedores = Fornecedor.objects.all()
    ped = Pedido.objects.get(id=pk)
    if request.method == "POST":
        form = PedidoForm(request.POST, instance=ped)
        #print(form.is_valid)
        if form.is_valid():
            ped = form.save(commit=False)
            ped.fornecedor = form.cleaned_data['fornecedor']
            ped.numero = form.cleaned_data['numero']
            ped.data = form.cleaned_data['data']
            ped.data_previsao = form.cleaned_data['data_previsao']
            ped.prazo = form.cleaned_data['prazo']
            ped.prazo_medio = form.cleaned_data['prazo_medio']
            ped.loja = form.cleaned_data['loja']
            ped.total = form.cleaned_data['total']
            ped.status = form.cleaned_data['status']
            ped.bonificacao = form.cleaned_data['bonificacao']
            ped.frete = form.cleaned_data['frete']
            ped.observacao = form.cleaned_data['observacao']

            ped.save()
            messages.success(request, 'Pedido atualizado com sucesso!')
            return redirect('pedido')
    else:
        form = PedidoForm(instance=ped)
    return render(request, 'ped_edita.html', {'form': form, 'ped': ped, 'fornecedores': fornecedores,})

@login_required(login_url='/login/')
def ped_deleta(request, pk):
    ped = Pedido.objects.get(id=pk)
    ped.delete()
    messages.error(request, 'Pedido excluido com sucesso!')
    return redirect('pedido')

@login_required(login_url='/login/')
def fornecedor(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, 'fornecedor.html', {'fornecedores': fornecedores})

@login_required(login_url='/login/')
def forn_novo(request):
    if request.method == "POST":
        form = FornecedorForm(request.POST)
        if form.is_valid():
            fornecedor = form.save(commit=False)
            fornecedor.razao = form.cleaned_data['razao']
            fornecedor.cnpj = form.cleaned_data['cnpj']
            fornecedor.save()
            messages.success(request, 'Fornecedor cadastrado com sucesso!')
            return redirect('fornecedor')
    else:
        form = FornecedorForm()
    return render(request, 'fornecedor.html', {'form': form})

@login_required(login_url='/login/')
def forn_edita(request, pk):
    forn = Fornecedor.objects.get(id=pk)
    #print(forn)
    if request.method == "POST":
        form = FornecedorForm(request.POST, instance=forn)
        #print(form.is_valid)
        if form.is_valid():
            forn = form.save(commit=False)
            forn.id = forn.id
            forn.razao = form.cleaned_data['razao']
            forn.cnpj = form.cleaned_data['cnpj']
            forn.save()
            messages.success(request, 'Fornecedor atualizado com sucesso!')
            return redirect('fornecedor')
    else:
        form = FornecedorForm(instance=forn)
    return render(request, 'forn_edita.html', {'form': form, 'forn': forn})

@login_required(login_url='/login/')
def forn_deleta(request, pk):
    fornecedor = Fornecedor.objects.get(id=pk)
    fornecedor.delete()
    messages.error(request, 'Fornecedor excluido com sucesso!')
    return redirect('fornecedor')

@login_required(login_url='/login/')
def classificacao(request, pkd):
    dado = DadosPedido.objects.get(id=pkd)
    ped = Pedido.objects.get(numero=dado.pedido)

    #print(dado.marca, dado.produto, dado.ref)
    pro = Produto.objects.filter(
        mar_pro_ref__mar = dado.marca,
        mar_pro_ref__pro = dado.produto,
        mar_pro_ref__ref = dado.ref,
    )

    if pro.exists():
        print(0)
    else:
        Produto.objects.create(mar_pro_ref={
            'mar': dado.marca,
            'pro': dado.produto,
            'ref': dado.ref,
        })

    pro = pro.get()

    clas = ClassificacaoProduto.objects.filter(prod=pro)
    #print(clas.exists())

    if clas.exists():
        clas = ClassificacaoProduto.objects.get(prod=pro)
        if request.method == "POST":
            form = ClassificacaoProdutoForm(request.POST, instance=clas)
            if form.is_valid():
                classi = form.save(commit=False)
                classi.prod = pro
                classi.secao = form.cleaned_data['secao']
                classi.sub_secao = form.cleaned_data['sub_secao']
                classi.estilo = form.cleaned_data['estilo']
                classi.formato = form.cleaned_data['formato']
                classi.superior = form.cleaned_data['superior']
                classi.abertura = form.cleaned_data['abertura']
                classi.membro = form.cleaned_data['membro']
                classi.detalhe = form.cleaned_data['detalhe']
                classi.material = form.cleaned_data['material']
                classi.save()

                messages.success(request, 'Classificacao criada com sucesso!')
                return redirect('ped_dados', pk=ped.id)
        else:
            form = ClassificacaoProdutoForm(instance=clas)
    else:
        if request.method == "POST":
            form = ClassificacaoProdutoForm(request.POST)
            if form.is_valid():
                classi = form.save(commit=False)
                classi.prod = pro
                classi.secao = form.cleaned_data['secao']
                classi.sub_secao = form.cleaned_data['sub_secao']
                classi.estilo = form.cleaned_data['estilo']
                classi.formato = form.cleaned_data['formato']
                classi.superior = form.cleaned_data['superior']
                classi.abertura = form.cleaned_data['abertura']
                classi.membro = form.cleaned_data['membro']
                classi.detalhe = form.cleaned_data['detalhe']
                classi.material = form.cleaned_data['material']
                classi.save()
                
                dado.status_class = True
                dado.save()
                messages.success(request, 'Classificacao criada com sucesso!')
                return redirect('ped_dados', pk=ped.id)
        else:
            form = ClassificacaoProdutoForm()
    
    return render(request, 'classificacao.html', {'dado':dado, 'form':form, 'ped':ped})

def login(request):
    if request.method == "POST":
        username = password = ''
        username = request.POST.get('usuario')
        password = request.POST.get('senha')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login_as(request, user)
                messages.success(request, 'Login realizado com sucesso!')
                return redirect('pedido')
        else:
            messages.error(request, 'Usuário ou senha incorretos')
            return redirect('login')
    else:
        return render(request, 'autenticacao/login.html', {})

def logout(request):
    logout_as(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('inicio')

@login_required(login_url='/login/')
def ped_dados(request, pk):
    ped = Pedido.objects.get(id=pk)
    dados = DadosPedido.objects.filter(pedido=ped)
    pedidos_all = Pedido.objects.filter(fornecedor=ped.fornecedor)

    class DadosPedidoForm(forms.ModelForm):

        def __init__(self, *args, **kwargs):
            super(DadosPedidoForm, self).__init__(*args, **kwargs)
            self.fields['pedido'].queryset = Pedido.objects.filter(numero=ped.numero)
            self.fields['quant_baixa'].disabled = True
            self.fields['quant_baixa'].initial = 0
            self.fields['preco_venda'].disabled = True
            self.fields['preco_venda'].initial = 0

        class Meta:
            model = DadosPedido
            fields = ('pedido', 'marca', 'produto', 'ref', 'tamanho', 'quant', 'quant_baixa', 'custo', 'icms', 'status', 'status_class', 'preco_venda',)
    
    DadosPedidoSetFormSet = modelformset_factory(DadosPedido, form=DadosPedidoForm, extra=0)
    formset = DadosPedidoSetFormSet(request.POST or None, queryset=dados)

    sum_pecas = dados.values('produto').annotate(Sum('quant'))
    #print(sum_pecas)

    pecas = 0
    for peca in sum_pecas:
        pecas = pecas + peca["quant__sum"]

    if request.method == "POST":
        if formset.is_valid():
            formset.save()
            #print(len(connection.queries))
            messages.success(request, 'Dados do Pedido atualizado com sucesso!')

            c = 0
            for d in dados:
                c = c + (d.custo*d.quant)
            
            ped.total = c
            ped.save()

            for form in formset:
                class_status = Produto.objects.filter(mar_pro_ref__mar=form.instance.marca).filter(mar_pro_ref__pro=form.instance.produto).filter(mar_pro_ref__ref=form.instance.ref)
            
                #print(form.instance.id)

                dado = DadosPedido.objects.get(id=form.instance.id)
                ped = Pedido.objects.get(numero=dado.pedido)
                par = Parametro.objects.get(id=38)

                if dado.icms == 12.00:
                    icms = float(par.icms_fora)
                elif dado.icms == 4.00:
                    icms = float(par.icms_importado)
                else:
                    icms = float(par.icms_minas)

                ipi = float(0)
                markup = float(par.markup)
                custo = float(dado.custo)
                desconto = float(ped.desconto)
                frete = float(ped.frete/ped.total)
                prazo = float(ped.prazo_medio)
                taxa = float(par.taxa)
                #print(ipi, markup, icms, custo, desconto, frete, prazo)

                valor = custo * (1 - (0.01 * desconto)) * (1 - (icms / 100) + (0.01 * frete) + (0.01 * ipi) / (1 - (0.01 * desconto))) * ((1 + (0.01 * taxa)) ** ((135 - prazo) / 30)) * markup

                dado.preco_venda = valor
                dado.save()

                if class_status.exists():
                    #print(form.instance.id)
                    #print(class_status)
                    dado = DadosPedido.objects.get(id=form.instance.id)
                    dado.status_class = True
                    dado.save()
            
            return redirect('ped_dados', pk=ped.id)
    else:
        formset = DadosPedidoSetFormSet(queryset=dados)
    
    return render(request, 'ped_dados.html', {'dados':dados, 'ped':ped, 'formset':formset, 'pecas':pecas, 'pedidos_all':pedidos_all})

@login_required(login_url='/login/')
def copiar_pedido(request, pk):
    ped = Pedido.objects.get(id=pk)
    if request.method == "POST":
        pk_copia = request.POST.get('id_ped')
        ped_copia = DadosPedido.objects.filter(pedido_id=pk_copia)
        for p_c in ped_copia:
            DadosPedido.objects.create(pedido=ped, marca=p_c.marca, produto=p_c.produto, ref=p_c.ref, tamanho=p_c.tamanho, quant=p_c.quant, quant_baixa=0, custo=p_c.custo, icms=p_c.icms, status=False, status_class=False, preco_venda=0)

        return redirect('ped_dados', pk=ped.id)

@login_required(login_url='/login/')
def baixar_todo_pedido(request, pk):
    ped = Pedido.objects.get(id=pk)
    ped_dados = DadosPedido.objects.filter(pedido_id=pk)
    for dado in ped_dados:
        #print(dado.quant)
        dado.quant_baixa = dado.quant
        dado.status = True
        dado.save()

        ped.status = 'QI'
        ped.save()
    return redirect('ped_dados', pk=ped.id)

@login_required(login_url='/login/')
def ped_dados_deleta(request, pkp, pkd):
    ped = Pedido.objects.get(id=pkp)
    dado = DadosPedido.objects.get(id=pkd)
    dados = DadosPedido.objects.filter(pedido=ped)
    dado.delete()

    c = 0
    for d in dados:
        c = c + (d.custo*d.quant)
    
    ped.total = c
    ped.save()

    messages.error(request, 'Dado excluido com sucesso!')
    return redirect('ped_dados', pk=ped.id)

@login_required(login_url='/login/')
def baixa(request):
    if request.method == "POST":
        pkd = request.POST.get('id')
        baixa = request.POST.get('baixa')
        
        dado = DadosPedido.objects.get(id=pkd)
        ped = Pedido.objects.get(numero=dado.pedido)

        baixa = int(baixa) + dado.quant_baixa

        dado.quant_baixa = baixa

        if int(dado.quant_baixa) - int(dado.quant) == 0:
            dado.status = True
            dado.save()
        else:
            dado.save()
        
        sum_quant = DadosPedido.objects.filter(pedido=ped).values('produto').annotate(Sum('quant'))
        sum_quant_baixa = DadosPedido.objects.filter(pedido=ped).values('produto').annotate(Sum('quant_baixa'))

        #print(sum_quant)

        s_q = 0
        s_q_b = 0

        for q in sum_quant:
            s_q = s_q + int(q["quant__sum"])

        for qb in sum_quant_baixa:
            s_q_b = s_q_b + int(qb["quant_baixa__sum"])
        
        #print(s_q)
        #print(s_q_b)

        if s_q == s_q_b:
            ped.status = 'QI'
        elif s_q_b > 0 and s_q_b < s_q:
            ped.status = 'PA'
        elif s_q_b == 0:
            ped.status = 'LA'
        
        ped.save()
        
        return redirect('ped_dados', pk=ped.id)

from django.db import connection

def sql_dado(l):
    sum_dado = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT produto, SUM(quant) as quant__sum, SUM(quant_baixa) as quant_baixa__sum FROM sistema_dadospedido WHERE pedido_id IN (SELECT id from sistema_pedido WHERE loja = %s) GROUP BY produto;", [l])
        row = cursor.fetchall()
        for r in row:
            sum_dado.append({
                'produto': r[0],
                'quant__sum': r[1],
                'quant_baixa__sum': r[2]
            })

    return sum_dado

def sql_dado2(l):
    count_ped_card = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT pedido_id, SUM(custo) FROM sistema_dadospedido WHERE pedido_id IN (SELECT id from sistema_pedido WHERE loja = %s) GROUP BY pedido_id;", [l])
        row = cursor.fetchall()
        for r in row:
            count_ped_card.append({
                'pedido_id': r[0],
                'custo': r[1],
            })

    return count_ped_card

@login_required(login_url='/login/')
def relatorio(request):
    ped = Pedido.objects.all()
    forn = Fornecedor.objects.all()

    quant_prod = 0
    count_ped_card = 0
    total_preco = 0

    if 'q' in request.GET and request.GET.get('q') != '':
        q = request.GET['q']
        ped = Pedido.objects.get(numero=q)
        sum_dado = DadosPedido.objects.filter(pedido=ped).values('produto').annotate(Sum('quant')).annotate(Sum('quant_baixa'))
        count_ped_card = 1
        total_preco_aux = Pedido.objects.get(numero=q)
        total_preco = total_preco_aux.total
    elif 'q' in request.GET and request.GET.get('q') == '':
        loja = request.GET['loja']
        if loja != '00':
            sum_dado = sql_dado(loja)
            count_ped_card = len(sql_dado2(loja))
            total_preco_aux = Pedido.objects.all().filter(loja=loja)
            for t in total_preco_aux:
                total_preco = total_preco + t.total
        else:
            sum_dado = DadosPedido.objects.values('produto').annotate(Sum('quant')).annotate(Sum('quant_baixa'))
            count_ped_card = len(Pedido.objects.all())
            total_preco_aux = Pedido.objects.all()
            for t in total_preco_aux:
                total_preco = total_preco + t.total
    else:
        sum_dado = DadosPedido.objects.values('produto').annotate(Sum('quant')).annotate(Sum('quant_baixa'))
        count_ped_card = len(Pedido.objects.all())
        total_preco_aux = Pedido.objects.all()
        for t in total_preco_aux:
            total_preco = total_preco + t.total
    #print(sum_dado)

    labels_forn = []
    dados_forn = []

    if 'q' in request.GET and request.GET.get('q') != '':
        q = request.GET['q']
        count_ped = Pedido.objects.values('fornecedor').annotate(Sum('total', distinct=True)).filter(numero=q)
    elif 'q' in request.GET and request.GET.get('q') == '':
        loja = request.GET['loja']
        if loja != '00':
            count_ped = Pedido.objects.values('fornecedor').annotate(Sum('total', distinct=True)).filter(loja=loja)
        else:
            count_ped = Pedido.objects.values('fornecedor').annotate(Sum('total', distinct=True))
    else:
        count_ped = Pedido.objects.values('fornecedor').annotate(Sum('total', distinct=True))
    #print(count_ped)

    for c in count_ped:
        forn_razao = Fornecedor.objects.get(id=int(c["fornecedor"]))
        dados_forn.append(float(c["total__sum"]))
        labels_forn.append(forn_razao.razao)

    labels_ped = []
    dados_ped = []

    for c in sum_dado:
        if int(c["quant__sum"])-int(c["quant_baixa__sum"]) > 0:
            labels_ped.append(c["produto"])
            dados_ped.append(int(c["quant__sum"])-int(c["quant_baixa__sum"]))
        
        quant_prod = quant_prod + c["quant__sum"]

    cores = []
    coresb = []
    
    for i in range(10):
        r = []
        r.append(randrange(255))
        r.append(randrange(255))
        r.append(randrange(255))
        r.append(0.2)
        r.append(1)

        cores.append(f'rgba({r[0]},{r[1]},{r[2]},{r[3]})')
        coresb.append(f'rgba({r[0]},{r[1]},{r[2]},{r[4]})')
    
    #print(cores)
    #print(coresb)

    context={
        'ped':ped,
        'forn':forn,
        'labels_forn':labels_forn,
        'dados_forn':dados_forn,
        'labels_ped':labels_ped,
        'dados_ped':dados_ped,
        'cores':cores,
        'coresb':coresb,
        'quant_prod':quant_prod,
        'count_ped_card':count_ped_card,
        'total_preco':total_preco,
    }
    return render(request, 'relatorio.html', context)

import io
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os
import locale

@login_required(login_url='/login/')
def imprimir(request, pk):
    ped = Pedido.objects.get(id=pk)
    dado = DadosPedido.objects.filter(pedido=ped).order_by('id')

    sum_pecas = dado.values('produto').annotate(Sum('quant'))
    #print(sum_pecas)

    pecas = 0
    for peca in sum_pecas:
        pecas = pecas + peca["quant__sum"]

    c = 0
    for d in dado:
        c = c + (d.custo*d.quant)

    b = 0
    for d in dado:
        b = b + (d.custo*d.quant_baixa)

    liquido = 0
    liquido = (ped.total * ((100-ped.desconto) / 100)) - ped.bonificacao + ped.frete

    if ped.loja == '01':
        loja = str('ZIZI COMÉRCIO') 
    elif ped.loja == '02':
        loja = str('ZIZI CONFECÇÕES')
    elif ped.loja == '04':
        loja = str('ZIZI ROSÁRIO')
    else:
        loja = str('ZIZI MODA ÍNTIMA')

    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize=letter)

    #cores
    #p.setStrokeColorRGB(0.2,0.5,0.3)
    #p.setFillColorRGB(1,0,1)

    p.setLineWidth(.3)
    # draw some lines
    p.line(20,30,20,760)
    p.line(20,30,580,30)
    p.line(580,30,580,760)
    p.line(20,760,580,760)

    p.setFont('Helvetica', 12)
    p.drawString(260, 730,'PEDIDO DE COMPRA')
    
    logo = os.path.join(os.path.dirname(__file__),'static/images/logo.png')
    p.drawImage(logo,40,720,width=90,height=30,mask=None)

    locale.setlocale(locale.LC_ALL, '')

    p.line(20,710,580,710)

    p.drawString(60, 690,'Pedido nº:')
    p.drawString(130, 690, str(ped.numero))
    p.drawString(60, 670,'Fornecedor:')
    p.drawString(130, 670, str(ped.fornecedor))
    p.drawString(60, 650,'Loja:')
    p.drawString(130, 650, loja)
    p.drawString(60, 630,'Prazos:')
    p.drawString(130, 630, str(ped.prazo))
    p.drawString(60, 610,'Data:')
    p.drawString(130, 610, str(ped.data.strftime('%d/%m/%Y')))
    p.drawString(60, 590,'Previsão:')
    p.drawString(130, 590, str(ped.data_previsao.strftime('%d/%m/%Y')))

    #p.drawString(130, 610, str('Concluído') if ped.status else str('Aberto'))
    
    p.drawString(380, 690,'Peças Total:')
    p.drawString(460, 690, str(pecas))
    p.drawString(380, 670,'Valor Total:')
    p.drawString(460, 670, str('R$ ' + locale.currency(c, symbol=False, grouping=True)))
    p.drawString(380, 650,'Desconto:')
    p.drawString(460, 650, str(ped.desconto)+'%')
    p.drawString(380, 630,'Bonificação:')
    p.drawString(460, 630, str('R$ ' + locale.currency(ped.bonificacao, symbol=False, grouping=True)))
    
    if(request.user.is_superuser):
        p.drawString(380, 610,'Frete:')
        p.drawString(460, 610, str('R$ ' + locale.currency(ped.frete, symbol=False, grouping=True)))
        p.drawString(380, 590,'Valor Líquido:')
        p.drawString(460, 590, str('R$ ' + locale.currency(liquido, symbol=False, grouping=True)))
    else:
        p.drawString(380, 610,'Valor Líquido:')
        p.drawString(460, 610, str('R$ ' + locale.currency(liquido, symbol=False, grouping=True)))
        p.drawString(380, 590,'Valor Baixado:')
        p.drawString(460, 590, str('R$ ' + locale.currency(b, symbol=False, grouping=True)))

    p.setFont('Helvetica', 10)

    p.drawCentredString(85, 560, 'Produto')
    p.drawCentredString(180, 560, 'Marca')
    p.drawCentredString(260, 560, 'Referência')
    p.drawCentredString(340, 560, 'Tamanho')
    p.drawCentredString(401, 560, 'Quant')
    p.drawCentredString(433, 560, 'Baixa')
    p.drawCentredString(469, 560, 'Uni')
    p.drawCentredString(515, 560, 'Total')
    p.drawCentredString(555, 560, "ICMS")
    p.line(30, 557, 570, 557)

    p.drawCentredString(85, 560, 'Produto')
    p.drawCentredString(180, 560, 'Marca')
    p.drawCentredString(260, 560, 'Referência')
    p.drawCentredString(340, 560, 'Tamanho')
    p.drawCentredString(401, 560, 'Quant')
    p.drawCentredString(433, 560, 'Baixa')
    p.drawCentredString(469, 560, 'Uni')
    p.drawCentredString(515, 560, 'Total')
    p.drawCentredString(555, 560, "ICMS")
    p.line(30, 557, 570, 557)

    p.line(30,57,30,575)
    p.line(135,57,135,575)
    p.line(220,57,220,575)
    p.line(302,57,302,575)
    p.line(385,57,385,575)
    p.line(418,57,418,575)
    p.line(448,57,448,575)
    p.line(493,57,493,575)
    p.line(540,57,540,575)
    p.line(570,57,570,575)
    p.line(30, 575, 570, 575)
    
    i = 540
    for d in dado:
        p.drawString(35, i, str(d.produto[:15]))
        p.drawString(140, i, str(d.marca[:12]))
        p.drawString(223, i, str(d.ref[:12]))
        p.drawString(305, i, str(d.tamanho[:12]))
        p.drawRightString(405, i, str(d.quant))
        p.drawRightString(437, i, str(d.quant_baixa))
        p.drawRightString(489, i, locale.currency(d.custo, symbol=False, grouping=True))
        p.drawRightString(536, i, locale.currency(d.custo*d.quant, symbol=False, grouping=True))
        p.drawRightString(568, i, str(d.icms))
        p.line(30, i-3, 570, i-3)
        i = i-20
        if i < 60:
            p.showPage()
            
            p.setLineWidth(.3)
            # draw some lines
            p.line(20,30,20,760)
            p.line(20,30,580,30)
            p.line(580,30,580,760)
            p.line(20,760,580,760)

            p.setFont('Helvetica', 10)

            p.drawCentredString(85, 720, 'Produto')
            p.drawCentredString(180, 720, 'Marca')
            p.drawCentredString(260, 720, 'Referência')
            p.drawCentredString(340, 720, 'Tamanho')
            p.drawCentredString(401, 720, 'Quant')
            p.drawCentredString(433, 720, 'Baixa')
            p.drawCentredString(469, 720, 'Uni')
            p.drawCentredString(515, 720, 'Total')
            p.drawCentredString(555, 720, "ICMS")
            p.line(30, 717, 570, 717)

            p.drawCentredString(85, 720, 'Produto')
            p.drawCentredString(180, 720, 'Marca')
            p.drawCentredString(260, 720, 'Referência')
            p.drawCentredString(340, 720, 'Tamanho')
            p.drawCentredString(401, 720, 'Quant')
            p.drawCentredString(433, 720, 'Baixa')
            p.drawCentredString(469, 720, 'Uni')
            p.drawCentredString(515, 720, 'Total')
            p.drawCentredString(555, 720, "ICMS")
            p.line(30, 717, 570, 717)

            p.line(30,57,30,735)
            p.line(135,57,135,735)
            p.line(220,57,220,735)
            p.line(302,57,302,735)
            p.line(385,57,385,735)
            p.line(418,57,418,735)
            p.line(448,57,448,735)
            p.line(493,57,493,735)
            p.line(540,57,540,735)
            p.line(570,57,570,735)
            p.line(30, 735, 570, 735)

            i = 700

    p.drawCentredString(295, 40, '------------------------------------------ Fim do Pedido ------------------------------------------')

    p.showPage()
    p.save()

    buffer.seek(0)

    return FileResponse(buffer, as_attachment=False, filename='pedido.pdf')