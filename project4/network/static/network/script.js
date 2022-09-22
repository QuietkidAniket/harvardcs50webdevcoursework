
document.addEventListener('click', event => {
    const element = event.target
    const parentelement_id = element.parentElement.id
    if(element.id === 'like' || element.id === 'liked'){
        
        fetch('/setlike?post_id='+parentelement_id)
        .then(response => response.json())
        .then(data => {
            console.log('This is like')
            document.querySelector('#no_of_likes_'+parentelement_id).innerHTML = `${data.nooflikes}`
        });

    }
    if(element.id === 'dislike' || element.id === 'disliked'){
        fetch('/setdislike?post_id='+parentelement_id)
    .then(response => response.json())
    .then(data => {
        console.log('This is dislike')
        document.querySelector('#no_of_dislikes_'+parentelement_id).innerHTML = `${data.noofdislikes}`
    });
    }
    if(element.id  === 'follow' || element.id === "unfollow"){
        const parentelement = element.parentElement
        const username  = parentelement.id 
        fetch(`/follow/${username}`);
        console.log('follow/unfollow request')
        window.location.reload()

    }
});

