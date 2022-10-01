
    
    document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#time').style.opacity = 0.5;
    document.querySelector('#stop').hidden = "hidden";
    document.querySelector('#answer').disabled = true;        
    document.querySelector('#ans_btn').disabled = true;
    document.querySelector("#diflev").disabled = true;
    document.querySelector("#restart").hidden = "hidden";
    document.querySelector("#numpad").hidden = "hidden";
    });
    
    function submitq(){
        ans = document.querySelector("#answer").value;
        answer = document.querySelector('#timevar').className;
        fetch('/game?state=put&answer='+ans+'&correctans='+answer)

        .then(response => response.json())
        .then(message => {
            
            s = message.state;
            if(s.localeCompare('Incorrect') == 0){
            document.querySelector('#answer').value = "";
            document.querySelector('.box').style.borderColor = "red";
        
            }else if(s.localeCompare('Correct') == 0){
                document.querySelector('#answer').value = "";
                document.querySelector('.box').style.borderColor = "green";
                getq();
            }
    
        });
        
        
    }

    function getq(){
        
            fetch('/game?state=get')
            .then(response => response.json())
            .then(d=>{
                document.querySelector("#timevar").className = d.ans;
                document.querySelector("#dq").innerHTML = d.a + " "+ d.sign +" "+d.b +" = ?";
            });
                
    }

document.addEventListener('click', event =>{
    const element = event.target;
    
    if(element.className === 'btn btn-primary num'){
        
        if(element.id === 'delete'){
        document.querySelector('#answer').value = (parseInt(parseInt(document.querySelector('#answer').value) / 10)).toString();}
        else if(element.title === "negativesign"){
            document.querySelector('#answer').value = (parseInt(parseInt(parseInt(document.querySelector('#answer').value) * (-1)))).toString();
        }
        else {
            document.querySelector('#answer').value = document.querySelector('#answer').value + element.value;
        }
    }
    
    
    }
    
);


    

document.addEventListener('keypress', event => {
    if (event.key === 'Enter'){
        
        submitq();
    }
});


    var timecounter = 0;
    function resumetimer(){
        document.querySelector('#answer').disabled = false;
        document.querySelector('#ans_btn').disabled = false;
        document.querySelector('#stop').hidden = null;
        document.querySelector('#time').style.opacity = 1;
        document.querySelector('#answer').focus();
        document.querySelector('#resume').hidden= "hidden";
        document.querySelector("#numpad").hidden = null;
        document.querySelector("#dq").hidden = null;
        document.querySelector('.box').style.borderColor = "green";
        var countDownDate = new Date( new Date().getTime() + timecounter);
                x= setInterval(function() {
            
            // Get current time
            var now = new Date().getTime();
            
            
            // Find the distance between now and the count down date
            var distance = countDownDate - now;
            // Time calculations for days, hours, minutes and seconds
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);
            var milli = Math.floor((distance % 1000 )/10);
            // Display the result in the element with id="demo"
            document.querySelector("#time").innerHTML = minutes + " : " + seconds + " : "+ milli;

            //if the pause button is clicked
            document.querySelector("#stop").onclick = () => {
            clearInterval(x);    
            timecounter = distance;
            document.querySelector("#resume").hidden = null;
            document.querySelector("#stop").hidden = "hidden";
            document.querySelector('.box').style.borderColor = "rgb(69, 114, 211)";
            document.querySelector('#answer').disabled = true;
            document.querySelector('#ans_btn').disabled = true;
            document.querySelector("#numpad").hidden = "hidden";
            document.querySelector('#dq').hidden = "hidden";
            };
            // If the count down is finished
            if (distance < 0) {
                clearInterval(x);
                document.querySelector("#time").innerHTML = "TIME UP";
                document.querySelector("#time").style.color = "rgb(211, 71, 71)";
                document.querySelector("#time").parentElement.style.borderStyle = "solid"; 
                document.querySelector("#time").parentElement.style.borderColor = "rgb(211, 71, 71)";
                document.querySelector("#stop").disabled = true;
                document.querySelector('.box').style.borderColor = "rgb(69, 114, 211)";
                document.querySelector('#answer').disabled = true;
                document.querySelector("#numpad").hidden = "hidden";
            document.querySelector('#ans_btn').disabled = true;
            document.querySelector('#dq').hidden = "hidden";
            }
            }, 1);
    }
    function starttimer(){
        time = document.querySelector("#timevar").value;
        time= time*1000
        console.log(time)
        getq();
    document.querySelector("#message").hidden = "hidden";
    document.querySelector('#time').style.opacity = 1;
    document.querySelector('#stop').hidden = null;
    document.querySelector('#start').hidden = "hidden";
    document.querySelector('#answer').disabled = false;
    document.querySelector('#answer').focus();                
    document.querySelector('#ans_btn').disabled = false;
    document.querySelector("#diflev").disabled = false;
    document.querySelector("#numpad").hidden = "";
    document.querySelector("#dq").hidden = "";    
    document.querySelector('.box').style.borderColor = "green";
        const start = new Date();
        var countDownDate = new Date(start.getTime() + time);
            // Update the count down every 1 second
            x= setInterval(function() {
                
            // Get current time
            var now = new Date().getTime();
            // Find the distance between now and the count down date
            var distance = countDownDate - now;
        
            // Time calculations for days, hours, minutes and seconds
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);
            var milli = Math.floor((distance % 1000 )/10);
            // Display the result in the element with id="demo"
            document.querySelector("#time").innerHTML = minutes + " :: " + seconds + " :: "+ milli;
            
            //if the pause button is clicked
            document.querySelector("#stop").onclick = () => {
            clearInterval(x);  
            timecounter = distance;  
            document.querySelector("#resume").hidden = null;
            document.querySelector("#stop").hidden = "hidden";
            document.querySelector('.box').style.borderColor = "rgb(69, 114, 211)";
            document.querySelector('#answer').disabled = true;
            document.querySelector('#ans_btn').disabled = true;
            document.querySelector("#numpad").hidden = "hidden";
            document.querySelector("#dq").hidden = "hidden";
            };

            // If the count down is finished
            if (distance < 0) {
                document.querySelector("#numpad").hidden = "hidden";
                clearInterval(x);
                document.querySelector("#time").innerHTML = "TIME UP";
                document.querySelector("#time").style.color = "rgb(211, 71, 71)";
                document.querySelector("#time").parentElement.style.borderStyle = "solid"; 
                document.querySelector("#time").parentElement.style.borderColor = "rgb(211, 71, 71)";
                document.querySelector("#stop").disabled = true;
                document.querySelector('.box').style.borderColor = "rgb(69, 114, 211)";
                document.querySelector('#answer').disabled = true;
                document.querySelector("#numpad").hidden = "hidden";
            document.querySelector('#ans_btn').disabled = true;
            document.querySelector('#dq').hidden = "hidden";
            }
            }, 1);
            
        }


