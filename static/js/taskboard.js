"use strict";

// Set due date minimum
let isoStringArray = new Date().toISOString().split(':')
let isoString = isoStringArray[0] + ':' + isoStringArray[1]

document.querySelector('#id_due_date').min = isoString


let editTaskButtons = document.querySelectorAll('.edit-task-button')
let taskForm_secondary = document.querySelector('#taskForm-secondary')
let createTaskForm = document.querySelector('#createTaskForm')

let btn = document.querySelectorAll('#taskForm-secondary .btn')


function removeAllChild(){
    let updateform_input_box = document.querySelectorAll('#taskForm-secondary .input-box')
    updateform_input_box.forEach(element =>{
        element.remove()
    })
    let btn = document.querySelectorAll('#taskForm-secondary .btn')
    if(btn){
        btn.forEach(element=>{
            element.remove()
        })
            
    }
}



function fetchUpdateForm(task_id){
    let url = `/update-task/${task_id}`
    taskForm_secondary.setAttribute("action", url)
    removeAllChild()

    fetch(url)
    .then(reponse => reponse.text())
    .then(html =>{
        taskForm_secondary.innerHTML += html;
    })
}



Array.from(editTaskButtons).forEach(editbtn =>{
    editbtn.addEventListener("click", function (){
        let task_id = this.dataset.task_id
        createTaskForm.style.display = 'none';
        fetchUpdateForm(task_id)
    })
    console.log(editbtn)
})



// Delete Task
let deleteTaskBtns = document.querySelectorAll('.delete-task-button')

Array.from(deleteTaskBtns).forEach(btn =>{
    btn.addEventListener("click", function (){
        btn.parentElement.classList.add('hidden')
        btn.parentElement.nextElementSibling.classList.remove('hidden')

        btn.parentElement.nextElementSibling.querySelector('.btn-cancel').addEventListener("click", ()=>{
            btn.parentElement.classList.remove('hidden')
            btn.parentElement.nextElementSibling.classList.add('hidden')
        })
    })
})