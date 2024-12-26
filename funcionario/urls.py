from django.urls import path, include
from .views import homepage, lista_colaboradores, cadastrar_colaborador, editar_colaborador, excluir_colaborador
from .views import editar_cargo, excluir_cargo, lista_cargos, cadastrar_cargo
from certificado.views import certificados_vencendo
urlpatterns = [
    path('', homepage, name='homepage'),
    path('listacolaboradores/', lista_colaboradores, name='lista_colaboradores'),
    path('cadastrar/', cadastrar_colaborador, name='cadastrar_colaborador'),
    path('editar/<int:pk>/', editar_colaborador, name='editar_colaborador'),
    path('excluir/<int:pk>/', excluir_colaborador, name='excluir_colaborador'),
    path('listacargos/', lista_cargos, name='lista_cargos'),
    path('cadastrarcargos/', cadastrar_cargo, name='cadastrar_cargo'),
    path('editarcargo/<int:pk>/', editar_cargo, name='editar_cargo'),
    path('excluircargo/<int:pk>/', excluir_cargo, name='excluir_cargo'),
    path('certificados_vencendo/', certificados_vencendo, name='certificados_vencendo')

]