from django import forms
from .models import Certificado, LancamentoCertificado
from funcionario.models import Funcionario

from django import forms
from .models import Certificado

# forms.py

from django import forms
from .models import Certificado

class CertificadoForm(forms.ModelForm):
    class Meta:
        model = Certificado
        fields = ['nome', 'validade_meses']





from django import forms
from .models import LancamentoCertificado




class LancamentoCertificadoForm(forms.ModelForm):
    class Meta:
        model = LancamentoCertificado
        fields = ['funcionario', 'certificado', 'data_realizacao', 'arquivo']

    def clean_certificado(self):
        certificado = self.cleaned_data.get('certificado')
        if not certificado:
            raise forms.ValidationError("O campo certificado é obrigatório.")
        return certificado

