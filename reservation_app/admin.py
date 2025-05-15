from django.contrib import admin
from .models import Employe, Administrateur, Salle, Equipement, Reservation

admin.site.register(Employe)
admin.site.register(Administrateur)
admin.site.register(Salle)
admin.site.register(Equipement)
admin.site.register(Reservation)
