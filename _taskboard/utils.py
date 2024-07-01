from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate(request, taskList):
    paginator = Paginator(taskList, 5)
    page = request.GET.get('page')
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        list = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        list = paginator.page(page)
    
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
        
    return list, custom_range