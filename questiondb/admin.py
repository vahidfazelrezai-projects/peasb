from django.contrib import admin
from questiondb.models import Round, Subject, Question

# Creates admin interface for Round
class RoundAdmin(admin.ModelAdmin):
    fields = ['name', 'author', 'pub_date']

# Makes these models editable on admin interface 
admin.site.register(Round, RoundAdmin)
admin.site.register(Subject)
admin.site.register(Question)
