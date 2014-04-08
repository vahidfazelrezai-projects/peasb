from django import forms

from questiondb.models import Round, Question, Subject

# Form for creating new Round
class RoundForm(forms.ModelForm):
    class Meta:
        model = Round
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'})
        }

# Form for adding Question to existing Round
class RoundEditForm(forms.ModelForm):
    question_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Question ID'}))

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

class RoundDeleteForm(forms.Form):
    round_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Round ID'}))

    def is_valid(self):
        valid = super(RoundDeleteForm, self).is_valid()
        if not valid: 
            return valid
        try:
            Round.objects.get(id=self.cleaned_data['round_id'])
        except Round.DoesNotExist:
            return False
        return True

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
        widgets = {
            'question_type': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'question_format': forms.Select(attrs={'class': 'form-control'}),
            'question': forms.Textarea(attrs={'class': 'form-control'}),
            'answer': forms.TextInput(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'citation': forms.TextInput(attrs={'class': 'form-control'}),
        }

class QuestionSelectForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.Select(attrs={'onchange': 'filter()', 'class': 'form-control'}))

class RoundOrderForm(forms.Form):
    question_list = forms.CharField(widget=forms.TextInput({'id': 'question_list', 'style': 'display: none;'}))
