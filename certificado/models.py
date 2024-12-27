from django.db import models
from funcionario.models import Funcionario  # Importando o modelo de Funcionário
from datetime import timedelta
import os




class Certificado(models.Model):
    nome = models.CharField(max_length=255)  # Nome do Certificado
    validade_meses = models.IntegerField()  # Validade em meses
    

    def __str__(self):
        return f"{self.nome} - {self.validade_meses} meses"






def upload_to_funcionario(instance, filename):
    # Obtém o nome do funcionário e nome do certificado
    nome_funcionario = instance.funcionario.nome.replace(" ", "_")  # Substitui espaços por underscores
    nome_certificado = instance.certificado.nome.replace(" ", "_")  # Substitui espaços por underscores
    # Formata a data de realização (no formato 'YYYY-MM-DD')
    data_realizacao = instance.data_realizacao.strftime('%Y-%m-%d')
    # Extrai a extensão do arquivo
    extension = filename.split('.')[-1]
    # Cria o novo nome de arquivo incluindo a data
    new_filename = f"{nome_funcionario}_{nome_certificado}_{data_realizacao}_certificado.{extension}"
    # Cria a pasta específica para o funcionário, se não existir
    directory = os.path.join('certificados', nome_funcionario)
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Retorna o caminho completo para salvar o arquivo dentro da pasta do funcionário
    return os.path.join(directory, new_filename)






class LancamentoCertificado(models.Model):
    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.CASCADE,
        related_name='lancamentos_certificados_atual'
    )
    certificado = models.ForeignKey(Certificado, on_delete=models.CASCADE)
    data_realizacao = models.DateField()
    validade_final = models.DateField(editable=False)
    arquivo = models.FileField(upload_to=upload_to_funcionario)

    def save(self, *args, **kwargs):
        # Verifica se o objeto já existe no banco de dados
        if self.id:
            # Obtém o objeto existente para verificar se o arquivo já foi carregado
            old_obj = LancamentoCertificado.objects.get(id=self.id)
            old_file_path = old_obj.arquivo.path if old_obj.arquivo else None
            if old_file_path and os.path.exists(old_file_path):
                # Deleta o arquivo anterior, se existir
                os.remove(old_file_path)

        # Sobrescreve qualquer lançamento existente para o mesmo funcionário e certificado
        LancamentoCertificado.objects.filter(
            funcionario=self.funcionario, certificado=self.certificado
        ).exclude(id=self.id).delete()

        # Calcula a validade final
        self.validade_final = self.data_realizacao + timedelta(days=self.certificado.validade_meses * 30)

        # Salva o lançamento
        super(LancamentoCertificado, self).save(*args, **kwargs)

