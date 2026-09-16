from django.contrib import admin

from .models import Campania
from .models import CentroSalud
from .models import Estado_Campania

admin.site.register(Campania)
admin.site.register(CentroSalud)
admin.site.register(Estado_Campania)
