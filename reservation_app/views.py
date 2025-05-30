
from django.shortcuts import render, redirect , get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.timezone import now
from .models import Reservation, Salle, Equipement, Employe
from datetime import datetime,timedelta,timezone

def base(request):
    return render(request, 'base.html')



def reserver(request):
    if request.method == 'POST':
        salle = Salle.objects.get(id=request.POST.get('room'))
        employe = Employe.objects.first()  
        date_debut = datetime.strptime(f"{request.POST['date']} {request.POST['start_time']}", "%Y-%m-%d %H:%M")
        date_fin = datetime.strptime(f"{request.POST['date']} {request.POST['end_time']}", "%Y-%m-%d %H:%M")

        reservation = Reservation.objects.create(
            employe=employe,
            salle=salle,
            date_debut=date_debut,
            date_fin=date_fin
        )

        reservation.equipements.set(request.POST.getlist('equipment'))

        return render(request, 'confirmaton.html') 

    
    salles = Salle.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'reservation.html', {
        'salles': salles,
        'equipements': equipements
    })

def auth(request):
    error = None 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('reserver')
        else:
            error = "Identifiants invalides."  

    return render(request, 'login.html', {'error': error})
def confirmation(request):
    return render(request,'confirmaton.html')


def rechercher(request):
    salles_disponibles = []

    if request.method == 'POST':
        date = request.POST.get('date')
        heure_debut = request.POST.get('start_time')
        heure_fin = request.POST.get('end_time')
        nom_salle = request.POST.get('nom_salle')
        capacite = request.POST.get('capacite')

        if date and heure_debut and heure_fin:
            debut = datetime.strptime(f"{date} {heure_debut}", "%Y-%m-%d %H:%M")
            fin = datetime.strptime(f"{date} {heure_fin}", "%Y-%m-%d %H:%M")

            salles = Salle.objects.all()

            if nom_salle:
                salles = salles.filter(nom__icontains=nom_salle)
            if capacite:
                salles = salles.filter(capacite__gte=capacite)

            for salle in salles:
                conflits = Reservation.objects.filter(
                    salle=salle,
                    date_debut__lt=fin,
                    date_fin__gt=debut
                )
                if not conflits.exists():
                    salles_disponibles.append(salle)

    return render(request, 'rechercher.html', {
        'salles_disponibles': salles_disponibles,
    })


def impression(request):
    periode = 'semaine' 
    today = now().date()

    if periode == 'mois':
        debut = today.replace(day=1)
        if debut.month == 12:
            fin = debut.replace(year=debut.year+1, month=1, day=1) - timedelta(days=1)
        else:
            fin = debut.replace(month=debut.month+1, day=1) - timedelta(days=1)
    else:
        debut = today - timedelta(days=today.weekday())
        fin = debut + timedelta(days=6)

    
    salles = Salle.objects.all()

    
    planning = {}
    for salle in salles:
        reservations = Reservation.objects.filter(
            salle=salle,
            date_debut__date__gte=debut,
            date_fin__date__lte=fin
        ).order_by('date_debut')
        planning[salle] = reservations

    context = {
        'planning': planning,
        'debut': debut,
        'fin': fin,
        'periode': periode,
    }
    return render(request, 'impression.html', context)
