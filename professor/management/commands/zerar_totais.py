from django.core.management.base import BaseCommand
from django.utils import timezone
from ...models import Usuario, Contagem
from ... import snmp


class Command(BaseCommand):
    help = 'Zerar cotas dos professores'
    def handle(self, *args, **kwargs):
   		professores = Usuario.objects.filter(tipo="professor")
   		professores.update(quantidade_atual=0)
   		instance = Contagem.objects.create(contagem= snmp.getTotalGeral())
   		instance.save()



   		