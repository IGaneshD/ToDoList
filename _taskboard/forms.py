from django import forms
from .models import Task
from django.forms import widgets

class taskCreationForm(forms.ModelForm):
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']

        widgets = {
            'due_date':forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

        labels = {
            'title':"Title",
            'description':"Description (optional)",
            'due_date':"Add a due date"
        }
    
    def __init__(self, *args, **kwargs):
        super(taskCreationForm, self).__init__(*args, **kwargs)

        self.fields['description'].widget.attrs.update({'rows':7})

        
