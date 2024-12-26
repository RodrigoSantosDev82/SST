from django.shortcuts import render, redirect, get_object_or_404
from .models import Funcionario,  Cargo
from .forms import FuncionarioForm, CargoForm
from certificado.views import certificados_vencendo
from django.db.models import Q


def homepage(request):

    return render(request, "homepage.html")


def lista_colaboradores(request):
    query = request.GET.get('q', '')  # Captura o valor do parâmetro de busca
    colaboradores = Funcionario.objects.filter(Q(nome__icontains=query)) if query else Funcionario.objects.all()
    return render(request, "colaboradores.html", {'colaboradores': colaboradores, 'query': query})


def cadastrar_colaborador(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            # Verificando o cargo
            cargo = form.cleaned_data.get('cargo')
            if not cargo:
                form.add_error('cargo', 'O campo cargo é obrigatório.')  # Adicionando erro específico
                return render(request, 'cadastrar_colaborador.html', {'form': form})

            form.save()
            return redirect('lista_colaboradores')  # Redireciona para lista de colaboradores
        else:
            # Se o formulário não for válido, renderize novamente com erros
            return render(request, 'cadastrar_colaborador.html', {'form': form})
    else:
        form = FuncionarioForm()
    return render(request, 'cadastrar_colaborador.html', {'form': form})




def editar_colaborador(request, pk):
    colaborador = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=colaborador)
        if form.is_valid():
            form.save()
            return redirect('lista_colaboradores')
    else:
        form = FuncionarioForm(instance=colaborador)
    return render(request, 'editar_colaborador.html', {'form': form})

def excluir_colaborador(request, pk):
    colaborador = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        colaborador.delete()
        return redirect('lista_colaboradores')
    return render(request, 'excluir_funcionario.html', {'colaborador': colaborador})


def lista_cargos(request):
    cargos = Cargo.objects.all()
    return render(request, 'lista_cargos.html', {'cargos': cargos})

def cadastrar_cargo(request):
    if request.method == 'POST':
        form = CargoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_cargos')
    else:
        form = CargoForm()
    return render(request, 'cadastrar_cargo.html', {'form': form})

def editar_cargo(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk)
    if request.method == 'POST':
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            return redirect('lista_cargos')
    else:
        form = CargoForm(instance=cargo)
    return render(request, 'editar_cargo.html', {'form': form})

def excluir_cargo(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk)
    if request.method == 'POST':
        cargo.delete()
        return redirect('lista_cargos')
    return render(request, 'excluir_cargo.html', {'cargo': cargo})

def clean_cargo(self):
    cargo = self.cleaned_data.get('cargo')
    if not cargo:
        raise forms.ValidationError("Este campo é obrigatório.")
    return cargo