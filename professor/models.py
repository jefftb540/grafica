# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class UsuarioManager(BaseUserManager):
    def create_user(self, matricula, password=None):
       
    	user = self.model(matricula=matricula)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matricula, password):
       
        user = self.create_user(matricula, password=password)
        user.is_superuser = True
        user.save(using=self._db)
        return user



class Usuario(AbstractBaseUser, PermissionsMixin):
	"""docstring for ClassName"""
		
	nome = models.CharField(max_length=30)
	matricula = models.CharField(max_length=14,  unique=True)
	quantidade_maxima = models.IntegerField(null=True, blank=True)
	quantidade_atual = models.IntegerField(default=0)
	tipo = models.CharField(max_length=9, choices=[['coapac','COAPAC'],['grafica','Grafica'],['professor','Professor']],default='professor')
	#is_superuser = models.BooleanField(default=False)

	@property
	def is_staff(self):
		return True

	def get_short_name(self):
		return self.nome

	objects = UsuarioManager()

	USERNAME_FIELD = 'matricula'
	def __str__(self):
		return self.nome

	


class Solicitacao(models.Model):
	professor = models.ForeignKey(Usuario)
	descricao = models.CharField(max_length=200, verbose_name="Descrição")
	totalFolhas = models.IntegerField(verbose_name = "Quantidade de Laudas" )
	totalAlunos = models.IntegerField(verbose_name = "Quantidade de Alunos" )
	totalGeral = models.IntegerField(null=True, blank=True, )
	impresso = models.BooleanField(default=False)
	aprovado = models.BooleanField(default=False)
	pendente = models.BooleanField(default=True)
	frente_verso = models.BooleanField(default=True, verbose_name = "Frente e Verso")
	data_solicitacao  = models.DateTimeField(editable=False, auto_now_add=True)
	arquivo = models.FileField(null=True, blank=True)
	professor_message = models.TextField(max_length=200, null=True, blank=True, verbose_name="Observação")
	coapac_message = models.TextField(max_length=200, null=True, blank=True, verbose_name="Observação")
	coapac_message_author = models.ForeignKey(Usuario, related_name="coapac_message_author", null=True, default=0)
	grafica_message = models.TextField(max_length=200, null=True, blank=True, verbose_name="Observação")
	grafica_message_author = models.ForeignKey(Usuario, related_name="grafica_message_author", null=True, default=0)

	
