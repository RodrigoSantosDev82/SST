from django import forms
from .models import Funcionario, Cargo


class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'cargo', 'matricula', 'data_admissao']

    def __init__(self, *args, **kwargs):
        super(FuncionarioForm, self).__init__(*args, **kwargs)
        self.fields['cargo'].queryset = Cargo.objects.all()  # Certificando-se de que os cargos estão populados

    def clean_cargo(self):
        cargo = self.cleaned_data.get('cargo')
        if not cargo:
            raise forms.ValidationError('O campo cargo é obrigatório.')  # Erro personalizado
        return cargo



class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ['nome']
