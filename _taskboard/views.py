from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from .forms import taskCreationForm
from django.contrib.auth.decorators import login_required
from .models import Task
import json
from django.template.loader import render_to_string
# from django.core.serializers import serialize

# Create your views here.
@login_required(login_url='signin')
def taskboard(request):
    tasks = Task.objects.filter(user = request.user)
    createTaskForm = taskCreationForm()
    updateTaskForms = {str(task.task_id):taskCreationForm(instance=task) for task in tasks}
    context = {'myTasks':tasks, 'createTaskForm':createTaskForm, 'updateTaskForms':updateTaskForms}

    return render(request, 'taskboard/taskboard.html', context)



@login_required(login_url='signin')
def create_task(request):
    if request.method == 'POST':
        form = taskCreationForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            return redirect('taskboard')

@login_required(login_url='signin')
def update_task(request, pk):
    task = Task.objects.get(task_id = pk)
    form = taskCreationForm(instance=task)

    if request.method == 'POST':
        form = taskCreationForm(request.POST, instance=task)

        if form.is_valid():
            form = form.save()
            return redirect('taskboard')
    
    context = {
        'updateForm':form,
        'task_id':task.task_id
    }
    html = render_to_string('taskboard/update-task-Form.html', context=context)
    return HttpResponse(html)


@login_required(login_url='signin')
def delete_task(request, pk):
    task = Task.objects.get(task_id = pk)
    if request.method == "POST":
        task.delete()
        return redirect('taskboard')

