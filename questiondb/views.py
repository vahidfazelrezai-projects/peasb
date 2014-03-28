import time

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from questiondb.models import Round, Question, RoundForm, RoundEditForm, RoundDeleteForm, QuestionForm, QuestionSelectForm

# Index page. Lists all existing rounds
@login_required(login_url='/login/')
def index(request):
    return render(request, 'questiondb/index.html')

#@login_required(login_url='/login/')
@staff_member_required
def list_rounds(request):
    rounds = Round.objects.all()
    return render(request, 'questiondb/list_rounds.html', {'rounds': rounds})

# View for viewing round and adding questions to round
@login_required(login_url='/login/')
#@staff_member_required
def view_round(request, round_id):
    # List of success/failure messages to return
    status = []
    if request.method == 'POST':
        form = RoundEditForm(request.POST)
        if form.is_valid():
            question = Question.objects.get(id=form.cleaned_data['question_id'])
            # Check that question isn't already in the round we're trying to add to
            if question.problemset == None or question.problemset.id != long(round_id):
                rd = Round.objects.get(id=round_id)
                # Makes question numbers good (in case of deletions)
                rd.fix()
                # Sets index equal to number of questions currently in round
                question.index = rd.question_set.count()
                question.problemset = rd
                question.save()
                # Sleep to give database time to update
                time.sleep(0.1)
                status.append('Success!')
            else:
                status.append('That question is already in here!')
        else:
            status.append("Something's wrong. :(")

    r = get_object_or_404(Round, pk=round_id)
    # If user is not staff, and round is not public, return 404.
    if r.public == False and request.user.is_staff == False:
        raise Http404

    form = RoundEditForm(instance=r)
    return render(request,
                  'questiondb/view_round.html',
                  {'form': form, 'round': r, 'status': status})

# View for creating new round
#login_required(login_url='/login/')
@staff_member_required
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
    return render(request,
                  'questiondb/add_round.html',
                  {'form': form})

# View for adding new question
@login_required(login_url='/login/')
def add_question(request):
    # List of success/failure messages to return
    status = []
    form = QuestionForm()
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
                difficulty = form.cleaned_data['difficulty'],
                author = request.user,
                pub_date = timezone.now()
            )
            q.save()
            status.append('Success!')
        else:
            status.append("Something's wrong. :(")
    return render(request,
                  'questiondb/add_question.html',
                  {'form': form, 'status': status})

# View for viewing unassigned questions, supports filtering by subject. 
# For viewing assigned questions, one should use admin page
@login_required(login_url='/login/')
def list_questions(request):
    subject = None
    if request.method == 'POST':
        form = QuestionSelectForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
    questions = None
    form = None
    if subject == None:
        questions = Question.objects.filter(problemset=None).order_by('-pub_date')
        form = QuestionSelectForm()
    else:
        questions = Question.objects.filter(problemset=None,
                                            subject=subject).order_by('-pub_date')
        form = QuestionSelectForm(initial={'subject':subject.id})
    return render(request,
                  'questiondb/list_questions.html',
                  {'questions': questions, 'form': form})

@staff_member_required
def delete_round(request):
    status = []
    if request.method == 'POST':
        form = RoundDeleteForm(request.POST)
        if form.is_valid():
            round_id = form.cleaned_data['round_id']
            rd = Round.objects.get(id=round_id)
            rd.delete()
            status.append('Success!')
        else:
            status.append("Something's wrong. :(")
    form = RoundDeleteForm()
    return render(request,
                  'questiondb/delete_round.html',
                  {'form': form, 'status': status})

@staff_member_required
def admin(request):
    return render(request, 'questiondb/admin.html')

