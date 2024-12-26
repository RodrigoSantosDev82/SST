from django.urls import path, include
from .views import lista_certificados, cadastrar_certificado, editar_certificado, excluir_certificado, lancar_certificado, lista_lancamentos_certificados, relatorio_alerta_certificados
from .views import certificados_vencendo
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.conf.urls.static import static




urlpatterns = [
    path('listacertificados', lista_certificados, name='lista_certificados'),
    path('cadastrarcertificado/', cadastrar_certificado, name='cadastrar_certificado'),
    path('editarcertificado/<int:pk>/', editar_certificado, name='editar_certificado'),
    path('excluircertificado/<int:pk>/', excluir_certificado, name='excluir_certificado'),
    path('lancarcertificado/', lancar_certificado, name='lancar_certificado'),
    path('listalancamentocertificado/', lista_lancamentos_certificados, name='lista_lancamentos_certificados'),
    path('relatorio-alerta/', relatorio_alerta_certificados, name='relatorio_alerta_certificados'),
    path('relatorio-alerta/pdf/', views.exportar_pdf, name='exportar_pdf'),
    path('grafico', certificados_vencendo, name='certificados_vencendo'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
