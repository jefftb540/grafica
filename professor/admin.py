from django.contrib import admin
from .models import Usuario
from .models import Solicitacao
from .models import Contagem

admin.site.register(Usuario)
admin.site.register(Solicitacao)
admin.site.register(Contagem)