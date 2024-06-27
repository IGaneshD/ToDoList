from django import forms
from .models import Task, Category


class taskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'important', 'category']

        widgets = {
            'due_date':forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

        labels = {
            'title':"Title (Required)",
            'description':"Description (optional)",
            'due_date':"Add a due date (Required)"
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['category'].queryset = Category.objects.filter(user=self.user)

        self.fields['description'].widget.attrs.update({'rows':7})

        self.fields['title'].widget.attrs.update({'required':True})
        self.fields['due_date'].widget.attrs.update({'required':True})

        # fetches categories belongs to logged in user
        
        
