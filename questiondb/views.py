import time

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from questiondb.models import Round, Question
from questiondb.forms import RoundForm, RoundEditForm, RoundDeleteForm, QuestionForm, QuestionSelectForm

# Index page. 
def index(request):
    return render(request, 'questiondb/index.html')

# View for adding new question
@login_required(login_url='/login/')
def add_question(request):
    # List of success/failure messages to return
    status = []
    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.pub_date = timezone.now()
            form.save()
            status.append(('Success!', 'label-success'))
            form = QuestionForm()
        else:
            status.append(("Something's wrong. :(", "label-danger"))
    return render(request,
                  'questiondb/add_question.html',
                  {'form': form, 'status': status})

@login_required(login_url='/login/')
def edit_question(request, question_id):
    status = []
    question = get_object_or_404(Question, pk=question_id)
    form = QuestionForm(instance=question);
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            status.append(('Success!', 'label-success'))
        else:
            status.append(("Something's wrong. :(", "label-danger"))
    if not request.user.is_staff and request.user != question.author:
        raise Http404
    return render(request,
                  'questiondb/edit_question.html',
                  {'form': form, 'status': status})

# View for viewing unassigned questions, supports filtering by subject. 
# For viewing assigned questions, one should use admin page
@login_required(login_url='/login/')
def list_questions(request):
    questions = Question.objects.filter(problemset=None).order_by('-pub_date')[:10]
    form = QuestionSelectForm()
    return render(request,
                  'questiondb/list_questions.html',
                  {'questions': questions, 'form': form, 'adj': 'New'})

@login_required(login_url='/login/')
def list_my_questions(request):
    questions = Question.objects.filter(author=request.user).order_by('-pub_date')
    form = QuestionSelectForm()
    return render(request,
                  'questiondb/list_questions.html',
                  {'questions': questions, 'form': form, 'adj': 'My'})

@staff_member_required
def list_all_questions(request):
    questions = Question.objects.filter(problemset=None).order_by('-pub_date')
    form = QuestionSelectForm()
    return render(request,
                  'questiondb/list_questions.html',
                  {'questions': questions, 'form': form, 'adj': 'All'})

#@login_required(login_url='/login/')
@staff_member_required
def list_rounds(request):
    rounds = Round.objects.all()
    return render(request, 'questiondb/list_rounds.html', {'rounds': rounds})

# View for viewing round and adding questions to round
@login_required(login_url='/login/')
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
                status.append(('Success!', 'label-success'))
            else:
                status.append(('That question is already in here!', 'label-danger'))
        else:
            status.append(("Something's wrong. :(", "label-danger"))

    r = get_object_or_404(Round, pk=round_id)
    # If user is not staff, and round is not public, return 404.
    if not r.public and not request.user.is_staff:
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

@staff_member_required
def delete_round(request):
    status = []
    if request.method == 'POST':
        form = RoundDeleteForm(request.POST)
        if form.is_valid():
            round_id = form.cleaned_data['round_id']
            rd = Round.objects.get(id=round_id)
            rd.delete()
            status.append(('Success!', 'label-success'))

        else:
            status.append(("Something's wrong. :(", "label-danger"))
    form = RoundDeleteForm()
    return render(request,
                  'questiondb/delete_round.html',
                  {'form': form, 'status': status})

@staff_member_required
def admin(request):
    return render(request, 'questiondb/admin.html')

@login_required(login_url='/login/')
def mod(request, round_id):
    r = get_object_or_404(Round, pk=round_id)
    if not r.public and not request.user.is_staff:
        raise Http404
    return render(request,
                  'questiondb/mod.html',
                  {'round': r})
