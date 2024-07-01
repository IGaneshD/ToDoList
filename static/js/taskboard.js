"use strict";

// Set due date minimum
let isoStringArray = new Date().toISOString().split(':')
let isoString = isoStringArray[0] + ':' + isoStringArray[1]

document.querySelector('#id_due_date').min = isoString

let paginateBtns = document.querySelectorAll('.paginator button')
let editTaskButtons = document.querySelectorAll('.edit-task-button')
let taskForm_secondary = document.querySelector('#taskForm-secondary')
let createTaskForm = document.querySelector('#createTaskForm')
let btn = document.querySelectorAll('#taskForm-secondary .btn')
let deleteTaskBtns = document.querySelectorAll('.delete-task-button')
let taskList = document.querySelector('.displayTasks')
let sidebar_links = document.querySelectorAll('.sidebar .sidebarLink')
let sidebar_categories = document.querySelectorAll('.sidebar button.sidebarLink-category p')
let deleteCategory = document.querySelectorAll('.category-name img')
let categories_display = document.querySelector('.categories_display')
let create_categories = document.querySelector('.create-cat')
let taskStatus = document.querySelectorAll('.task-status')

addPaginationEventListner()
deleteTaskEventListener()
editTaskEventListener()
deleteCategoryEventListener()
sidebar_categoriesEventListener()

function updateDOMVariables() {
    paginateBtns = document.querySelectorAll('.paginator button')
    editTaskButtons = document.querySelectorAll('.edit-task-button')
    taskForm_secondary = document.querySelector('#taskForm-secondary')
    createTaskForm = document.querySelector('#createTaskForm')
    btn = document.querySelectorAll('#taskForm-secondary .btn')
    deleteTaskBtns = document.querySelectorAll('.delete-task-button')
    taskList = document.querySelector('.displayTasks')
    sidebar_links = document.querySelectorAll('.sidebar .sidebarLink')
    sidebar_categories = document.querySelectorAll('.sidebar button.sidebarLink-category p')
    deleteCategory = document.querySelectorAll('.category-name img')
    categories_display = document.querySelector('.categories_display')
    create_categories = document.querySelector('.create-cat')
    taskStatus = document.querySelectorAll('.task-status')

    addPaginationEventListner()
    deleteTaskEventListener()
    editTaskEventListener()
    deleteCategoryEventListener()
    sidebar_categoriesEventListener()
    taskStatusEventListener()
}


// display Tasks

function fetchresult(query, page, type) {

    if (type == 'category') {
        let url = `/getCategories/?page=${page}`
        console.log(url)

        fetch(url)
            .then(response => response.text())
            .then(html => {
                categories_display.innerHTML = html;
                updateDOMVariables();
            });
    }
    else {
        let url = `/gettasks/?query=${query}&page=${page}`
        console.log(url)

        fetch(url)
            .then(response => response.text())
            .then(html => {
                taskList.innerHTML = html;
                updateDOMVariables();
            });
    }

}

function delCategory(category_id) {
    console.log(category_id)
    let url = `/deleteCategory/`
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        mode: 'same-origin',
        body: JSON.stringify({ 'category_id': `${category_id}` })
    })
        .then(response => response.text())
        .then(html => {
            categories_display.innerHTML = html
            updateDOMVariables()
        })

}

function handleCategoryDelete() {
    let category_id = this.dataset.id;
    let category = this.parentElement.parentElement;
    let category_name = this.parentElement;
    console.log(this)

    let catDeleteDiv = document.createElement('div');
    catDeleteDiv.className = 'confirm-category-delete';

    let catDeleteA1 = document.createElement('a');
    catDeleteA1.innerText = 'Confirm';

    let catDeleteA2 = document.createElement('a');
    catDeleteA2.innerText = 'Cancel';

    catDeleteDiv.appendChild(catDeleteA1);
    catDeleteDiv.appendChild(catDeleteA2);

    category.appendChild(catDeleteDiv);
    category_name.style.display = 'none';

    catDeleteA2.addEventListener('click', () => {
        catDeleteDiv.remove();
        category_name.style.display = 'flex';
    });

    catDeleteA1.addEventListener('click', () => {
        delCategory(category_id);
        catDeleteDiv.remove();
        category_name.style.display = 'flex';
    });
}




//delete category Event Listener
function deleteCategoryEventListener() {
    deleteCategory.forEach(category => {
        category.removeEventListener('click', handleCategoryDelete);
        category.addEventListener('click', handleCategoryDelete);
    });
}


function addPaginationEventListner() {
    // paginate using api
    Array.from(paginateBtns).forEach(element => {
        element.addEventListener('click', function () {
            console.log('clicked')
            let page = this.dataset.page
            let type = this.dataset.type
            let query = document.querySelector('.sidebar button.active').dataset.query

            fetchresult(query, page, type)
        })
    })
}

Array.from(sidebar_links).forEach(element => {
    element.addEventListener('click', function () {
        try{

            document.querySelector('.sidebar button.active').classList.remove('active')
        }
        finally{

            this.classList.add('active')
        }

        fetchresult(this.dataset.query, '')
    })
})

function sidebar_categoriesEventListener() {
    Array.from(sidebar_categories).forEach(element => {
        element.addEventListener('click', function () {
            try{

                document.querySelector('.sidebar button.active').classList.remove('active')
            }
            finally{

                this.parentElement.parentElement.classList.add('active')
            }
            console.log(this)
            fetchresult(this.dataset.query, '')
        })
    })
}







// Delete Task
function deleteTaskEventListener() {
    Array.from(deleteTaskBtns).forEach(btn => {

        btn.addEventListener("click", function () {
            console.log('clicked delete')
            btn.parentElement.classList.add('hidden')
            btn.parentElement.nextElementSibling.classList.remove('hidden')

            btn.parentElement.nextElementSibling.querySelector('.btn-cancel').addEventListener("click", () => {
                btn.parentElement.classList.remove('hidden')
                btn.parentElement.nextElementSibling.classList.add('hidden')
            })
        })
    })
}

function editTaskEventListener() {

    Array.from(editTaskButtons).forEach(editbtn => {
        editbtn.addEventListener("click", function () {
            console.log('clicked editbtn')
            let task_id = this.dataset.task_id
            createTaskForm.style.display = 'none';
            fetchUpdateForm(task_id)
        })
    })
}


function removeAllChild() {
    let updateform_input_box = document.querySelectorAll('#taskForm-secondary .input-box')
    updateform_input_box.forEach(element => {
        element.remove()
    })
    let btn = document.querySelectorAll('#taskForm-secondary .btn')
    if (btn) {
        btn.forEach(element => {
            element.remove()
        })
    }
    updateDOMVariables();
}


function fetchUpdateForm(task_id) {
    let url = `/update-task/${task_id}`
    taskForm_secondary.setAttribute("action", url)
    removeAllChild()

    fetch(url)
        .then(response => response.text())
        .then(html => {
            taskForm_secondary.innerHTML = html;
            updateDOMVariables();
        })
}


document.querySelector('.add-category').addEventListener('click', function () {
    taskForm_secondary.style.display = 'none'
    document.querySelector('.create-task').style.display = 'none'
    document.querySelector('.create-cat').style.display = 'flex'
})


function taskStatusEventListener(){

    Array.from(taskStatus).forEach(task=>{
        task.addEventListener('click', function (){
            let task_id = this.dataset.task_id
            console.log(task_id)
    
            let url = '/update-status/'
            const request = new Request(url, {
                'method':'POST',
                headers:{
                    'X-CSRFToken':csrftoken,
                },
                mode:'same-origin',
                body:JSON.stringify({'task_id':task_id})
            })
            
            fetch(request)
            .then(response => response.json())
            .then(result => {
                if(result){
                    console.log(result)
                    updateDOMVariables()
                }
            })
        })
    })
}
