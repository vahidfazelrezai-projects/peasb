from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Round(models.Model):
  name = models.CharField(max_length=200)
  author = models.ForeignKey(User)
  pub_date = models.DateField('date added')
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
      default='T'
      )
  subject = models.ForeignKey(Subject)
  question = models.TextField()
  answer = models.CharField(max_length=200)
  citation = models.CharField(max_length=200)
  pub_date = models.DateField('date added')
  author = models.ForeignKey(User)

  attempts = models.IntegerField(default=0, editable=False)
  corrects = models.IntegerField(default=0, editable=False)

  problemset = models.ForeignKey(Round)
  index = models.IntegerField(default=0)

  def __unicode__(self):
    return self.question
