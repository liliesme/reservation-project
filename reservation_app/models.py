from django.db import models
from django.contrib.auth.models import User

class Employe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Administrateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"Admin {self.user.username}"

class Salle(models.Model):
    nom = models.CharField(max_length=100)
    capacite = models.IntegerField()
    disponible = models.BooleanField(default=True)
    gerant = models.ForeignKey(Administrateur, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nom

class Equipement(models.Model):
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, related_name='equipements')

    def __str__(self):
        return f"{self.nom} ({self.type})"

class Reservation(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='reservations')
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, related_name='reservations')
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    equipements = models.ManyToManyField(Equipement, blank=True)

    def __str__(self):
        return f"{self.employe.user.username} -> {self.salle.nom} ({self.date_debut} à {self.date_fin})"
