//wait for the page to load 
document.addEventListener('DOMContentLoaded', function(){
    //store the references to the elements or select the text box and submit button
    const newTask = document.querySelector('#task');
    const submit = document.querySelector('#submit');
    //disable the submit button by default
    submit.disabled = true;
    //listen for input to be typed into the input field 
    newTask.onkeyup = function(){
        if(newTask.value.length > 0){
        submit.disabled = false;
        }else{
            submit.disabled = true;
        }
    }
    //listen for submission of form
    document.querySelector('form').onsubmit = function(){
        //find the task that the user just submitted
        const task = newTask.value;
        //create a list element for storing the value of the new task
        const li = document.createElement('li');
        li.innerHTML = task;
        //update the list
        document.querySelector('#tasklist').append(li);
        //reset the value of newTask to ''
        newTask.value = '';
        //disable the submit button again
        submit.disabled = true;
        //stop form from submitting
        return false;
    }
     
});