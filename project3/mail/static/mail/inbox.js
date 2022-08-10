document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click',  compose_email);
  document.querySelector('#compose-form').addEventListener('submit', compose_submit);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function compose_submit(event){
  //to prevent from the page from reloading 
  event.preventDefault()
  const recipients = document.querySelector("#compose-recipients").value;
    const subject = document.querySelector("#compose-subject").value;
    const body = document.querySelector("#compose-body").value;
  
    // Send the data to the server.
    fetch(`/emails`, {
      method: "POST", //post method sends data to the server
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
      }),
    })
      // Take the return data and parse it in JSON format.
      .then((response) => response.json())
      .then(() => {
        load_mailbox("sent");
      })
      
}


function load_email(email_id){
  fetch('/emails/' + email_id)
  .then(response => response.json())
  .then(email => {

    // show email and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';
    //refreshing the view
    document.querySelector('#email-view').innerHTML = '';
    // display email in the view
    const view = document.querySelector('#email-view');
    view.innerHTML = `
      <ul class="list-group">
        <li class="list-group-item"><b>From:</b> <span>${email['sender']}</span></li>
        <li class="list-group-item"><b>To: </b><span>${email['recipients']}</span></li>
        <li class="list-group-item"><b>Subject:</b> <span>${email['subject']}</span</li>
        <li class="list-group-item"><b>Time:</b> <span>${email['timestamp']}</span></li>
      </ul>
      <p class="m-2">${email['body']}</p>
    `;

    // create reply button & append to DOMContentLoaded
    const reply = document.createElement('button');
    reply.className = "btn btn-primary";
    reply.innerHTML = "Reply";
    reply.addEventListener('click', ()=>{
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#email-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'block';
      //setting all the pre-fills
      document.querySelector("#compose-recipients").value = email["sender"];
      document.querySelector("#compose-subject").value = ((email["subject"].match(/^(Re:)\s/)) ? email["subject"] : "Re: " + email["subject"]);
      document.querySelector("#compose-body").value = `On ${email["timestamp"]} ${email["sender"]} wrote:\n${email["body"]}\n-------------------------------------\n`;
      }
      );
    reply.style.position = "relative";
    reply.style.right = "10px";
    view.appendChild(reply);

    // create archive button & append to DOM
    archiveButton = document.createElement('button');
    archiveButton.className = "btn btn-primary";
    archiveButton.innerHTML = !email['archived'] ? 'Archive' : 'Unarchive';
    archiveButton.addEventListener('click', function() {
      fetch('/emails/' + email['id'], {
        method: 'PUT',
        body: JSON.stringify({ archived : !email['archived'] })
      })
      .then(response => load_mailbox('inbox'))
    });
    view.appendChild(archiveButton);

    // create mark as unread button & append to DOM
    readButton = document.createElement('button');
    readButton.className = "btn-secondary m-1";
    readButton.innerHTML = "Mark as Unread"
    readButton.addEventListener('click', function() {
      fetch('/emails/' + email['id'], {
        method: 'PUT',
        body: JSON.stringify({ read : false })
      })
      .then(response => load_mailbox('inbox'))
    })
    view.appendChild(readButton);

    // mark this email as read
    if (!email['read']) {
      fetch('/emails/' + email['id'], {
        method: 'PUT',
        body: JSON.stringify({ read : true })
      })
    }
  });
}

function load_mailbox(mailbox){
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  const view = document.querySelector('#emails-view');
  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;
  fetch('/emails/' + mailbox)
  .then(response => response.json())
  .then(emails => {

    emails.forEach((item) => {
      let parent_element = document.createElement('div');
      build_emails(item, parent_element, mailbox);
      parent_element.addEventListener("click", () => load_email(item["id"]));
          document.querySelector("#emails-view").appendChild(parent_element);
    })
  });
}
      
function build_emails(item, parent_element, mailbox){
    parent_element.style.backgroundColor = "rgb(226, 223, 223)"; 
    parent_element.style.borderStyle = "solid";
    parent_element.style.borderWidth = "2px";
    parent_element.style.margin = "10px";
    //don't show the emails which are archived and don't show the contents of archive-view
    if (mailbox === "inbox" && item["archived"]) {
      return;
    }
    else if (mailbox === "archive" && !item["archived"]) {
      return;
    }
    
    const content = document.createElement("div");
  
    const recipients = document.createElement("strong");
    //if the mailbox is sent-view then display all recipients, else display the sender
    if (mailbox === "sent") {
      recipients.innerHTML = item["recipients"].join(", ") + " ";
    }
    else {
      recipients.innerHTML = item["sender"] + " ";
    }
    content.appendChild(recipients);
    //adding/appending all the subjects
    content.innerHTML += item["subject"];
    
    const date = document.createElement("div");
    date.innerHTML = item["timestamp"];
    //adding style in displaying date
    date.style.display = "inline-block";
    date.style.float = "right";
    
    //if the email is read then set its color as greyish, else set date class to text muted
    if (item["read"]) {
      parent_element.style.backgroundColor = "white";
      parent_element.style.borderWidth = "1px";
      date.style.color = "black";
      date.className = "text-muted"
    }
    content.appendChild(date);
  
    content.style.padding = "10px";
    parent_element.appendChild(content);
  
  
    // Style the parent element.
    
}
  
