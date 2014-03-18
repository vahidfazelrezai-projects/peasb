from django.db import models
from django import forms
from django.contrib.auth.models import User

class Round(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(User, blank=True)
    pub_date = models.DateField('date added', blank=True)
    def __unicode__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class Question(models.Model):
    QUESTION_TYPES = (
        ('Toss-up', 'Toss-up'),
        ('Bonus', 'Bonus'),
    )
    question_type = models.CharField(
        max_length=7,
        choices=QUESTION_TYPES,
        default='Toss-up'
    )
    QUESTION_FORMATS = (
        ('Multiple Choice', 'Multiple Choice'),
        ('Short Answer', 'Short Answer'),
    )
    question_format = models.CharField(
        max_length=15,
        choices=QUESTION_FORMATS,
        default='Multiple Choice'
    )
    subject = models.ForeignKey(Subject, blank=True)
    question = models.TextField()
    answer = models.CharField(max_length=200)
    citation = models.CharField(max_length=200, blank=True)
    pub_date = models.DateField('date added')
    author = models.ForeignKey(User)

    attempts = models.IntegerField(default=0, editable=False)
    corrects = models.IntegerField(default=0, editable=False)

    problemset = models.ForeignKey(Round, null=True, blank=True)
    index = models.IntegerField(default=0)

    def __unicode__(self):
        ret =  (
            str(self.id) + ": " +
            self.question_type + " " +
            self.subject.__unicode__() + " " +
            self.question_format + " " +
            self.question[:30]
        )
        if len(self.question) > 30:
            ret += "..."
        return ret

class RoundForm(forms.ModelForm):
    class Meta:
        model = Round
        fields = ['name']

class RoundEditForm(forms.ModelForm):
    question_id = forms.IntegerField()
    class Meta:
        model = Round
        fields = []

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'question_type',
            'subject',
            'question_format',
            'question',
            'answer',
            'citation'
        ]
