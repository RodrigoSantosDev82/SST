from django.shortcuts import render, redirect, get_object_or_404
from .models import Certificado, LancamentoCertificado, Funcionario
from .forms import CertificadoForm, LancamentoCertificadoForm
from django.shortcuts import render, redirect
from datetime import date, datetime, timedelta
from django.utils.timezone import now as today
from funcionario.models import Funcionario
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import matplotlib.pyplot as plt
import io
import base64
import logging
import matplotlib
matplotlib.use('Agg')

def lista_certificados(request):
    certificados = Certificado.objects.all()
    return render(request, 'lista_certificados.html', {'certificados': certificados})


def cadastrar_certificado(request):
    if request.method == 'POST':
        form = CertificadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Salva o certificado
            return redirect('lista_certificados')  # Redireciona para a lista de certificados
    else:
        form = CertificadoForm()

    return render(request, 'cadastrar_certificado.html', {'form': form})

def editar_certificado(request, pk):
    certificado = get_object_or_404(Certificado, pk=pk)
    if request.method == 'POST':
        form = CertificadoForm(request.POST, instance=certificado)
        if form.is_valid():
            form.save()
            return redirect('lista_certificados')
    else:
        form = CertificadoForm(instance=certificado)
    return render(request, 'editar_certificado.html', {'form': form})

def excluir_certificado(request, pk):
    certificado = get_object_or_404(Certificado, pk=pk)
    if request.method == 'POST':
        certificado.delete()
        return redirect('lista_certificados')
    return render(request, 'excluir_certificado.html', {'certificado': certificado})

def lancar_certificado_old(request):
    if request.method == 'POST':
        form = LancamentoCertificadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Certifique-se de que o formulário salva apenas os campos válidos
            return redirect('lista_certificados')  # Redirecione após salvar
    else:
        form = LancamentoCertificadoForm()

    return render(request, 'lancar_certificado.html', {'form': form})

def lancar_certificado(request):
    if request.method == 'POST':
        form = LancamentoCertificadoForm(request.POST, request.FILES)
        if form.is_valid():
            # Obtém o objeto sem salvá-lo no banco
            novo_lancamento = form.save(commit=False)

            # Confirma o salvamento usando a lógica do método save do modelo
            novo_lancamento.save()

            return redirect('lista_lancamentos_certificados')
    else:
        form = LancamentoCertificadoForm()

    return render(request, 'lancar_certificado.html', {'form': form})

def clean_validade_meses(self):
    validade_meses = self.cleaned_data.get('validade_meses')
    if not validade_meses:
        raise forms.ValidationError("O campo validade_meses é obrigatório.")
    return validade_meses


def lista_lancamentos_certificados(request):
    # Captura o parâmetro de filtro
    funcionario_id = request.GET.get('funcionario', '')

    # Filtra os lançamentos se o funcionário for selecionado
    if funcionario_id:
        lancamentos = LancamentoCertificado.objects.filter(funcionario_id=funcionario_id)
    else:
        lancamentos = LancamentoCertificado.objects.all()

    # Lista de funcionários para o filtro
    funcionarios = Funcionario.objects.all()

    return render(request, 'lista_lancamentos.html', {
        'lancamentos': lancamentos,
        'funcionarios': funcionarios,
        'funcionario_id': funcionario_id,
    })

logger = logging.getLogger(__name__)

def certificados_vencendo(request):
    try:
        hoje = datetime.now().date()
        vencimento_limite = hoje + timedelta(days=30)

        expirado_count = LancamentoCertificado.objects.filter(validade_final__lt=hoje).count()
        proximo_count = LancamentoCertificado.objects.filter(validade_final__gte=hoje,
                                                             validade_final__lte=vencimento_limite).count()
        valido_count = LancamentoCertificado.objects.filter(validade_final__gte=vencimento_limite).count()

        total_colaboradores = Funcionario.objects.count()

        categorias = ['Expirado', 'Próximo a Vencer', 'Válido']
        valores = [expirado_count, proximo_count, valido_count]

        plt.figure(figsize=(6, 4))
        plt.bar(categorias, valores, color=['red', 'orange', 'green'])
        plt.title('Situação dos Certificados')
        plt.xlabel('Categoria')
        plt.ylabel('Quantidade')
        plt.tight_layout()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        grafico_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        plt.close()

        return render(request, 'certificados_vencendo.html', {
            'expirado_count': expirado_count,
            'proximo_count': proximo_count,
            'valido_count': valido_count,
            'grafico': grafico_base64,
            'total_colaboradores': total_colaboradores,
        })

    except Exception as e:
        logger.error(f"Erro ao gerar o gráfico: {e}")
        return render(request, 'certificados_vencendo.html', {
            'erro': f"Erro ao gerar o gráfico: {e}"
        })

# Exemplo de alerta_periodo e today para a lógica do filtro
today = date.today()
alerta_periodo = today + timedelta(days=30)

def relatorio_alerta_certificados(request):
    situacao = request.GET.get('situacao', 'todos')
    funcionario_id = request.GET.get('funcionario', '')

    # Base QuerySet
    lancamentos = LancamentoCertificado.objects.all()

    # Filtrar por situação
    hoje=datetime.now().date()
    alerta_periodo = hoje + timedelta(days=30)

    # Filtro por situação
    if situacao == 'valido':
        lancamentos = lancamentos.filter(validade_final__gte=today)
    elif situacao == 'proximo':
        lancamentos = lancamentos.filter(validade_final__lte=alerta_periodo, validade_final__gte=today)
    elif situacao == 'expirado':
        lancamentos = lancamentos.filter(validade_final__lt=today)

    # Filtro por funcionário
    if funcionario_id:
        lancamentos = lancamentos.filter(funcionario_id=funcionario_id)

    # Dados para o formulário
    funcionarios = Funcionario.objects.all()

    # Passando os dados para o template
    return render(request, 'relatorio_alerta_certificados.html', {
        'lancamentos': lancamentos,
        'situacao': situacao,
        'funcionarios': funcionarios,
        'hoje': today,
        'alerta_periodo': alerta_periodo,
    })

def exportar_pdf(request):
    situacao = request.GET.get('situacao', 'todos')
    lancamentos = LancamentoCertificado.objects.all()

    # Filtrar pela situação
    if situacao == 'valido':
        lancamentos = lancamentos.filter(validade_final__gte=date.today())
    elif situacao == 'proximo':
        alerta_periodo = date.today() + timedelta(days=30)
        lancamentos = lancamentos.filter(validade_final__range=(date.today(), alerta_periodo))
    elif situacao == 'expirado':
        lancamentos = lancamentos.filter(validade_final__lt=date.today())

    # Passar a data de hoje
    context = {
        'lancamentos': lancamentos,
        'situacao': situacao,
        'hoje': date.today(),  # Passando a data atual
    }

    # Renderizar o PDF
    html = render_to_string('relatorio_alerta_certificados_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_certificados.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response





