from django.db import models
from django import forms
from django.contrib.auth.models import User

class Round(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(User, blank=True)
    pub_date = models.DateField(blank=True)
    def __unicode__(self):
        return self.name

    def fix(self):
        # fixes question indices
        # for use when adding/deleting questions
        questions = list(self.question_set.order_by('index'))
        ind = 0
        for q in questions:
            q.index = ind
            q.save()
            ind += 1

    def delete(self):
        for question in self.question_set.all():
            question.problemset = None
            question.save()
        super(Round, self).delete()


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

    # Introductory = first year high school course
    # Intermediate = second year or AP
    # Advanced = beyond AP
    DIFFICULTIES = (
        (1, 'Introductory'),
        (2, 'Intermediate'),
        (3, 'Advanced'),
    )
    difficulty = models.IntegerField(
        choices = DIFFICULTIES,
        default = 2
    )

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
        try:
            Question.objects.get(id=self.cleaned_data['question_id'])
        except Question.DoesNotExist:
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
        if self.cleaned_data['difficulty'] == None:
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
            'difficulty',
            'citation'
        ]

class QuestionSelectForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.Select(attrs={'onchange': 'this.form.submit();'}))

class RoundDeleteForm(forms.Form):
    round_id = forms.IntegerField()

    def is_valid(self):
        valid = super(RoundDeleteForm, self).is_valid()
        if not valid: 
            return valid
        try:
            Round.objects.get(id=self.cleaned_data['round_id'])
        except Round.DoesNotExist:
            return False
        return True
