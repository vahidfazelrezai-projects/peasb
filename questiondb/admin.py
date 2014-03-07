from django.contrib import admin
from questiondb.models import Round, Subject, Question

class RoundAdmin(admin.ModelAdmin):
  fields = ['name', 'author', 'pub_date']

admin.site.register(Round, RoundAdmin)
admin.site.register(Subject)
admin.site.register(Question)
