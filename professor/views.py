# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms.models import modelform_factory
from django.shortcuts import render, redirect
from django.contrib.auth.views import login
from .forms import ProfessorForm
from django.contrib.auth.decorators import login_required, permission_required
from models import Solicitacao
from models import Usuario
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from . import snmp


# Create your views here.
@login_required
def index(request):
	solicitacoes = Solicitacao.objects.all().order_by('-id')
	if(request.user.tipo == "professor"):
		solicitacoes = solicitacoes.filter(professor = request.user)
		return render(request, "solicitacao/listar.html", {'solicitacoes' : solicitacoes})
	elif(request.user.tipo == "coapac"):
		totalnaoImpressas = solicitacoes.filter(impresso=False, aprovado=True).count()
		return render(request, "coapac/solicitacao/index.html", {'solicitacoes' : solicitacoes, 'naoImpressas': totalnaoImpressas})
	else:
		return render(request, "grafica/nao_impressas.html", {'solicitacoes' : solicitacoes})




@login_required
def listar(request):
	solicitacoes = Solicitacao.objects.all().order_by('-id')
	return render(request, "coapac/solicitacao/listar.html", {'solicitacoes' : solicitacoes})


@login_required
def naoImpressas(request):
	solicitacoes = Solicitacao.objects.all().order_by('-id')
	return render(request, "coapac/solicitacao/nao_impressas.html", {'solicitacoes' : solicitacoes})


@login_required
def pendentes(request):
	solicitacoes = Solicitacao.objects.all().order_by('-id')
	total = snmp.get('192.168.193.12',['.1.3.6.1.2.1.43.10.2.1.4.1.1'], hlapi.CommunityData('public'))
	return render(request, "coapac/solicitacao/pendentes.html", {'solicitacoes' : solicitacoes, 'totalImpressoes' : total})


def entrar(request):
	return login(request, template_name="login.html" )





solicitacaoForm = modelform_factory(Solicitacao, fields = ['descricao','totalFolhas','totalAlunos', 'arquivo', 'professor_message', 'frente_verso' ])
@login_required
@permission_required('professor.add_solicitacao')
def novaSolicitacao(request):
	if request.method == 'POST':
		form = solicitacaoForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.professor = request.user
			print instance.arquivo
			instance.totalGeral = instance.totalAlunos*instance.totalFolhas
			if((instance.totalGeral+instance.professor.quantidade_atual) < instance.professor.quantidade_maxima):
				instance.aprovado = True
				instance.pendente = False
				instance.coapac_message = "Solicitação aprovada automaticamente"
				instance.professor.quantidade_atual+= instance.totalGeral
				instance.professor.save()
			instance.save()
			messages.success(request, 'Solicitação Enviada')
			return redirect(reverse('index'))
		else:
			print "Formulário inválido"
	else:
		form = solicitacaoForm()
	
	return render(request, "solicitacao/form.html", {'form' : form})


CoapacMessageForm= modelform_factory(Solicitacao, fields = ['coapac_message' ])
@login_required
@permission_required('professor.change_solicitacao')
def criarMensagemCoapac(request, solicitacaoID):
	solicitacao = Solicitacao.objects.get(pk=solicitacaoID)
	if request.method == 'POST':
		form = CoapacMessageForm(request.POST, instance=solicitacao)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.coapac_message_author = request.user
			instance.save()
			messages.success(request, 'Solicitação Enviada')
			return redirect(reverse('index'))
		else:
			print "Formulário inválido"
	else:
		form = CoapacMessageForm(instance=solicitacao)
	
	return render(request, "solicitacao/form.html", {'form' : form})


GraficaMessageForm= modelform_factory(Solicitacao, fields = ['grafica_message' ])
@login_required
@permission_required('professor.change_solicitacao')
def criarMensagemGrafica(request, solicitacaoID):
	solicitacao = Solicitacao.objects.get(pk=solicitacaoID)
	if request.method == 'POST':
		form = GraficaMessageForm(request.POST, instance=solicitacao)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.grafica_message_author = request.user
			instance.save()

			messages.success(request, 'Solicitação Enviada')
			return redirect(reverse('index'))
		else:
			print "Formulário inválido"
	else:
		form = GraficaMessageForm(instance=solicitacao)
	
	return render(request, "solicitacao/form.html", {'form' : form})


@login_required
@permission_required('professor.change_solicitacao')
def aprovarSolicitacao(request, solicitacaoID):
	solicitacao = Solicitacao.objects.get(pk=solicitacaoID)
	solicitacao.aprovado = True
	solicitacao.pendente = False
	solicitacao.save()
	return redirect(reverse('criar_message_coapac', args=[solicitacaoID]))


@login_required
@permission_required('professor.change_solicitacao')
def negarSolicitacao(request, solicitacaoID):
	solicitacao = Solicitacao.objects.get(pk=solicitacaoID)
	solicitacao.pendente = False
	solicitacao.aprovado = False
	solicitacao.professor.quantidade_atual -= solicitacao.totalGeral
	solicitacao.save()
	return redirect(reverse('criar_message_coapac', args=[solicitacaoID]))


@login_required
@permission_required('professor.change_solicitacao')
def confirmar(request, solicitacaoID):
	solicitacao = Solicitacao.objects.get(pk=solicitacaoID)
	solicitacao.impresso = True
	solicitacao.save()
	return redirect(reverse('criar_message_grafica', args=[solicitacaoID]))


UsuarioForm = modelform_factory(Usuario, fields = ['tipo', 'matricula','nome', 'quantidade_maxima'])
@login_required
@permission_required('professor.add_usuario')
def cadastrarProfessor(request):
	if request.method == 'POST':
		form = UsuarioForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Professor Cadastrado')
			return redirect(reverse('listar_professores'))
		else:
			print "Formulário inválido"
	else:
		form = UsuarioForm()
	
	return render(request, "coapac/professor/form.html", {'form' : form})


@login_required
@permission_required('professor.change_usuario')
def editarProfessor(request, professorID):
	usuario = Usuario.objects.get(pk=professorID)
	if request.method == 'POST':
		form = UsuarioForm(request.POST, instance=usuario)
		if form.is_valid():
			form.save()
			messages.success(request, 'Professor Cadastrado')
			return redirect(reverse('listar_professores'))
		else:
			print "Formulário inválido"
	else:
		
		form = UsuarioForm(instance=usuario)
	
	return render(request, "coapac/professor/form.html", {'form' : form})



@login_required
@permission_required('professor.change_usuario')
def definirSenha(request, professorID):
	usuario = Usuario.objects.get(pk=professorID)
	if request.method == 'POST':
		form = AdminPasswordChangeForm(user=usuario, data=request.POST)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, 'Professor Cadastrado')
			return redirect(reverse('listar_professores'))
		else:
			print "Formulário inválido"
	else:
		
		form = AdminPasswordChangeForm(user=usuario)
	
	return render(request, "coapac/professor/form.html", {'form' : form})




@login_required
@permission_required('professor.add_usuario')
def listarProfessores(request):
	professores = Usuario.objects.filter(tipo="professor")
	return render(request,'coapac/professor/listar.html', {'professores': professores})

@login_required
@permission_required('professor.add_usuario')
def listarUsuarios(request):
	usuarios = Usuario.objects.exclude(tipo='professor')
	return render(request,'coapac/usuario/listar.html', {'usuarios': usuarios})





