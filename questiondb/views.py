import time

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from questiondb.models import Round, Question, RoundForm, RoundEditForm, QuestionForm

@login_required(login_url='/login/')
def index(request):
    rounds = Round.objects.all()
    return render(request, 'questiondb/index.html', {'rounds': rounds})

@login_required(login_url='/login/')
def view_round(request, round_id):
    if request.method == 'POST':
        form = RoundEditForm(request.POST)
        if form.is_valid():
            question = Question.objects.get(id=form.cleaned_data['question_id'])
            if question.problemset == None or question.problemset.id != long(round_id):
                question.index = Round.objects.get(id=round_id).question_set.count()
                question.problemset = Round.objects.get(id=round_id)
                question.save()
                time.sleep(0.1)
    r = get_object_or_404(Round, pk=round_id)
    form = RoundEditForm(instance=r)
    return render(request, 'questiondb/view_round.html', {'form': form, 'round': r})

@login_required(login_url='/login/')
def add_round(request):
    if request.method == 'POST':
        form = RoundForm(request.POST)
        if form.is_valid():
            r = Round(
                name = form.cleaned_data['name'],
                author = request.user,
                pub_date = timezone.now()
            )
            r.save()
            return HttpResponseRedirect('/qdb')
    else:
        form = RoundForm()
    return render(request, 'questiondb/add_round.html', {'form': form})

@login_required(login_url='/login/')
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = Question(
                question_type = form.cleaned_data['question_type'],
                subject = form.cleaned_data['subject'],
                question_format = form.cleaned_data['question_format'],
                question = form.cleaned_data['question'],
                answer = form.cleaned_data['answer'],
                citation = form.cleaned_data['citation'],
                author = request.user,
                pub_date = timezone.now()
            )
            q.save()
    form = QuestionForm()
    return render(request, 'questiondb/add_question.html', {'form': form})

def view_questions(request):
    questions = Question.objects.filter(problemset=None)
    return render(request, 'questiondb/view_questions.html', {'questions': questions})

