from django import forms
from .models import Task, Category

class TaskCreationForm(forms.ModelForm):
    """
    A form for creating a new Task instance.

    This form uses Django's built-in ModelForm to create a form that corresponds to the Task model.
    It includes fields for title, description, due date, importance, and category.

    The form also includes customizations for the due date field to use a datetime-local input,
    and for the category field to only show categories belonging to the current user.

    Parameters:
        user (django.contrib.auth.models.User): The current user, used to filter categories.

    Attributes:
        title (CharField): The title of the task.
        description (TextField): The description of the task.
        due_date (DateTimeField): The due date of the task.
        important (BooleanField): Whether the task is important.
        category (ModelChoiceField): The category of the task.
    """

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'important', 'category']

        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

        labels = {
            'title': "Title (Required)",
            'description': "Description (optional)",
            'due_date': "Add a due date (Required)"
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['category'].queryset = Category.objects.filter(user=self.user)

        self.fields['description'].widget.attrs.update({'rows': 7})

        self.fields['title'].widget.attrs.update({'required': True})
        self.fields['due_date'].widget.attrs.update({'required': True})
        

class CategoryCreationForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']