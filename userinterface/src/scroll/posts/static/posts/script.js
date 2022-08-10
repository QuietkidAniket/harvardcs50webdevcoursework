let counter = 1;
const quantity = 20;
document.addEventListener("DOMContentLoaded",load);
document.addEventListener('click', event => {
    const element = event.target;
    if(element.className === 'hide'){
        element.parentElement.style.animationPlayState = 'running';
        element.parentELement.addEventListener('animationend', () => {
            cdelement.parentElement.remove();
        });
    }
});

window.onscroll = ()=>{
    if(window.scrollY + window.innerHeight >= document.body.offsetHeight){
        load()
    }
}
function load(){
    const start =counter;
    const end = start + quantity - 1;
    counter = end +1;

    fetch(`/posts?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(data => {
        data.posts.forEach(add_post);
    })
}
function add_post(contents){
    //Create new post
    const post = document.createElement('div');
    post.className = 'post';
    post.innerHTML = `${contents} <button class= "hide">Hide</button>`;
    //Add post to DOM
    document.querySelector('#posts').append(post);
}