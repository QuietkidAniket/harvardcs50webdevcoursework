document.addEventListener('DOMContentLoader', function(){
    //send a GET request to the URl
    fetch('https://api.exchangeratesapi.io/latest?base=USD')
    //put response into json form
    .then(response => response.json())
    .then(data => {
        //log data to the console
        console.log(data);
        //get rate from the data
        const rate = data.rates.EUR;
        //display a message on the screen
        document.querySelector('body').innerHTML = "1 USD is equal to ${rate.tofixed(3)} EUR" 
    });
});