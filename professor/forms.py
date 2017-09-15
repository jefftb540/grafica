from django import forms
from .models import Usuario


class ProfessorPerfilForm(forms.ModelForm):
	class Meta:
		model = Usuario
		fields = ('nome', 'matricula', 'quantidade_maxima', 'quantidade_atual')


class ProfessorForm(ProfessorPerfilForm):
	password = forms.CharField(label='Senha', help_text='Use pelo menos 6 caracteres.',widget=forms.PasswordInput(), min_length=6)

	confirm_password = forms.CharField(label='Confirmar senha', help_text='Use pelo menos 6 caracteres.',  widget=forms.PasswordInput(), min_length=6
		)

	class Meta:
		model = Usuario
		fields = ('nome', 'matricula', 'quantidade_maxima', 'quantidade_atual'
		)
