document.addEventListener('click', event =>{
    const element = event.target;
    if(element.className === "btn btn-primary dif"){
        document.querySelector("#diftext").innerHTML = "<strong>Difficulty Level " + element.value + "</strong><br>" + element.title;
    }
});

