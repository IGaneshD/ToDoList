from django.shortcuts import render, HttpResponse, redirect
from .forms import TaskCreationForm
from django.contrib.auth.decorators import login_required
from .models import Task, Category
from django.template.loader import render_to_string
from .utils import paginate
from django.utils import timezone
from django.http import JsonResponse
import json
from django.contrib.auth.models import User


# Create your views here.
@login_required(login_url='signin')
def taskboard(request):
    user = request.user
    today = timezone.now().date()
    taskList = Task.objects.filter(user = request.user, due_date__date=today)
    categories = Category.objects.filter(user=request.user)
    num_categories = len(categories)
    
    tasks, custom_range = paginate(request, taskList)
    form = TaskCreationForm()
    context = {'myTasks':tasks, 'page_range':custom_range, 'createTaskForm':form, 'categories':categories, 'no_of_categories':num_categories}

    return render(request, 'taskboard/taskboard.html', context)

@login_required(login_url='signin')
def getTasks(request):
    query = request.GET.get('query')
    category = None
    try:
        _, category = query.split('_')
    except:
        pass
    
    if query=='important':
        display_title = 'Important'
        taskList = Task.objects.filter(user = request.user, important='Yes')
    elif query=='all':
        display_title = 'All'
        taskList = Task.objects.filter(user = request.user)
    elif query=='completed':
        display_title = 'Completed'
        taskList = Task.objects.filter(user=request.user, status='COMPLETED')
    elif query=='overdue':
        today = timezone.now().date()
        display_title='Over Due'
        taskList = Task.objects.filter(user=request.user, status='PENDING', due_date__date__lt=today)
    elif category:
        display_title = category
        taskList = Task.objects.filter(user=request.user, category__name=category)
        
    else:
        today = timezone.now().date()
        display_title = ''
        taskList = Task.objects.filter(user = request.user, due_date__date=today)
    
    
    tasks, custom_range = paginate(request, taskList)
    context = {
        'myTasks':tasks,
        'page_range':custom_range,
        'display_title':display_title,
        'type':'tasks'
    }
    html = render_to_string('taskboard/task-display.html', context=context, request=request)
    
    return HttpResponse(html)

@login_required(login_url='signin')
def updateTaskStatus(request):
    data = json.loads(request.body)
    task_id = data['task_id']
    taskStatus = data['status']
    print(taskStatus)
    task = Task.objects.get(task_id = task_id)
    if request.method == 'POST':
        if taskStatus=='PENDING':
            task.status = 'COMPLETED'
        else:
            task.status = 'PENDING'
        task.save()
    
    return JsonResponse({'completed':True}, safe=False)
        
    

@login_required(login_url='signin')
def creatCategory(request):
    if request.method=='POST':
        category = request.POST['name']
        category.capitalize()
        category = Category.objects.get_or_create(user=request.user, name = category)
        
        
    return redirect('taskboard')



@login_required(login_url='signin')
def create_task(request):
    if request.method == 'POST':
        form = TaskCreationForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            return redirect('taskboard')
        

@login_required(login_url='signin')
def update_task(request, pk):
    task = Task.objects.get(task_id = pk)
    form = TaskCreationForm(instance=task, user=request.user)

    if request.method == 'POST':
        form = TaskCreationForm(request.POST, instance=task)

        if form.is_valid():
            form = form.save()
            return redirect('taskboard')
    
    context = {
        'updateForm':form,
        'task_id':task.task_id
    }
    html = render_to_string('taskboard/update-task-Form.html', context=context, request=request)
    return HttpResponse(html)


@login_required(login_url='signin')
def delete_task(request, pk):
    task = Task.objects.get(task_id = pk)
    if request.method == "POST":
        task.delete()
        return redirect('taskboard')


@login_required(login_url='signin')
def deleteCategory(request):
    data = json.loads(request.body)
    pk = data['category_id']
    print(data)
    category = Category.objects.get(id=pk)
    
    if request.method=='POST':
        category.delete()
    
    return JsonResponse({'status':'deleted'}, safe=False)
    
    