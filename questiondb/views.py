# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from questiondb.models import Round

def index(request):
    rounds = Round.objects.all()
    return render(request, 'questiondb/index.html', {'rounds': rounds})

def view_round(request, round_id):
    r = get_object_or_404(Round, pk=round_id)
    return render(request, 'questiondb/view_round.html', {'round': r})
