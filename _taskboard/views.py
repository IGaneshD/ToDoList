from django.shortcuts import render, HttpResponse, redirect
from .forms import taskCreationForm
from django.contrib.auth.decorators import login_required
from .models import Task
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
@login_required(login_url='signin')
def taskboard(request):
    tasks = Task.objects.filter(user = request.user)

    paginator = Paginator(tasks, 5)
    page = request.GET.get('page')
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        tasks = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        tasks = paginator.page(page)
    
    custom_range = paginator.page_range

    if paginator.num_pages>=5:
        leftIndex = int(page) - 2
        rightIndex = int(page) + 2
        if leftIndex < 1:
            rightIndex = rightIndex - leftIndex + 1
            leftIndex = 1  
        # if int(page)==paginator.num_pages:
        #     leftIndex = paginator.num_pages - 4
        #     rightIndex = paginator.num_pages

        if rightIndex>paginator.num_pages:
            leftIndex = leftIndex - (2 - (paginator.num_pages - int(page)) )
            rightIndex = paginator.num_pages
    
        custom_range = range(leftIndex, rightIndex+1)

    form = taskCreationForm(user=request.user)
    context = {'myTasks':tasks, 'page_range':custom_range, 'createTaskForm':form}

    return render(request, 'taskboard/taskboard.html', context)



@login_required(login_url='signin')
def create_task(request):
    if request.method == 'POST':
        form = taskCreationForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            return redirect('taskboard')
        

@login_required(login_url='signin')
def update_task(request, pk):
    task = Task.objects.get(task_id = pk)
    form = taskCreationForm(instance=task, user=request.user)

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

