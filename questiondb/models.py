from django.db import models
from django import forms
from django.contrib.auth.models import User

class Round(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(User, blank=True)
    pub_date = models.DateField(blank=True)
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
        max_length = 7,
        choices = QUESTION_TYPES,
        default = 'Toss-up'
    )
    QUESTION_FORMATS = (
        ('Multiple Choice', 'Multiple Choice'),
        ('Short Answer', 'Short Answer'),
    )
    question_format = models.CharField(
        max_length = 15,
        choices = QUESTION_FORMATS,
        default = 'Multiple Choice'
    )
    subject = models.ForeignKey(Subject)
    question = models.TextField()
    answer = models.CharField(max_length=200)
    citation = models.CharField(max_length=200, blank=True)
    pub_date = models.DateField()
    author = models.ForeignKey(User)

    # attempts = models.IntegerField(default=0, editable=False)
    # corrects = models.IntegerField(default=0, editable=False)

    problemset = models.ForeignKey(Round, null=True, blank=True)
    # Represents position of Question in its round
    index = models.IntegerField(default=0)

    # Returns default way to display Question
    def __unicode__(self):
        ret =  (
            str(self.id) + ": " +
            self.question_type + " " +
            self.subject.__unicode__() + " " +
            self.question_format + " " +
            self.question
        )
        return ret

# Form for creating new Round
class RoundForm(forms.ModelForm):
    class Meta:
        model = Round
        fields = ['name']

# Form for adding Question to existing Round
class RoundEditForm(forms.ModelForm):
    question_id = forms.IntegerField()

    def is_valid(self):
        valid = super(RoundEditForm, self).is_valid()
        if not valid:
            return valid
        # Checks if question exists
        question = Question.objects.get(id=self.cleaned_data['question_id'])
        if question == None:
            return False
        return True

    class Meta:
        model = Round
        fields = []

# Form for adding new Question
class QuestionForm(forms.ModelForm):
    def is_valid(self):
        valid = super(QuestionForm, self).is_valid()
        if not valid:
            return valid
        # Checks that required fields are not empty
        if self.cleaned_data['subject'] == None:
            return False
        if self.cleaned_data['question'] == None:
            return False
        if self.cleaned_data['answer'] == None:
            return False
        return True
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

class QuestionSelectForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.Select(attrs={'onchange': 'this.form.submit();'}))
