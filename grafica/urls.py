# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""grafica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth  import views as auth
from professor import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index, name='index'),
    url(r'', views.index, name='index'),
    url(r'^login', views.login),
    url(r'^logout$', auth.logout_then_login, name='logout'),
    url(r'^solicitacao/criar/', views.novaSolicitacao, name='criar_solicitacao'),
    url(r'^listar/', views.listar, name='listar'),
    url(r'^coapac/solicitacao/aprovar/(\d+)$', views.aprovarSolicitacao, name='aprovar_solicitacao'),
    url(r'^coapac/solicitacao/negar/(\d+)$', views.negarSolicitacao, name='negar_solicitacao'),
    url(r'^coapac/solicitacao/pendentes/', views.pendentes, name='solicitacoes_pendentes'),
    url(r'^solicitacao/naoImpressas/', views.naoImpressas, name='solicitacoes_nao_impressas'),
    url(r'^solicitacao/confirmar/(\d+)$', views.confirmar, name='confirmar_impressao'),
    url(r'^coapac/professores/listar/', views.listarProfessores, name='listar_professores'),
    url(r'^coapac/professores/cadastrar/', views.cadastrarProfessor, name='cadastrar_professores'),
    url(r'^coapac/professores/editar/(\d+)$', views.editarProfessor, name='editar_professores'),
    url(r'^coapac/usuarios/listar/', views.listarUsuarios, name='listar_usuarios'),
    url(r'^coapac/professores/senha/(\d+)$', views.definirSenha, name='definir_senha'),
    url(r'^coapac/solicitacao/message/criar/(\d+)$', views.criarMensagemCoapac, name='criar_message_coapac'),
    url(r'^grafica/solicitacao/message/criar/(\d+)$', views.criarMensagemGrafica, name='criar_message_grafica'),
    

    
        
    #"""url(r'^alterar_senha/$', auth.password_change, name='password_change', kwargs={'template_name':'alterar_senha.html'})"""
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
