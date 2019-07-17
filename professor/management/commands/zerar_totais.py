from django.core.management.base import BaseCommand
from django.utils import timezone
from professor import models
from models import Usuario


class Command(BaseCommand):
    help = 'Zerar cotas dos professores'
    def handle(self, *args, **kwargs):
   		professores = Usuario.objects.filter(tipo="professor")
   		professores.update(quantidade_atual=0)
   		professores.save()