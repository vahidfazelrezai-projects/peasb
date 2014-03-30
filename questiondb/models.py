from django.db import models
from django.contrib.auth.models import User

class Round(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(User, blank=True)
    pub_date = models.DateField(blank=True)
    public = models.BooleanField(default=True)
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
    pub_date = models.DateTimeField()
    author = models.ForeignKey(User)

    problemset = models.ForeignKey(Round, null=True, blank=True, on_delete=models.SET_NULL)
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

