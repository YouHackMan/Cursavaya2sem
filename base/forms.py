from django import forms
from .models import Task
from .models import Hashtag

class TaskForm(forms.ModelForm):
    hashtags = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Hashtag.objects.all())
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'filter', 'hashtag'] 
        

