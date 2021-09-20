let chatInput = $('#chat-input');
let chatButton = $('#btn-send');
let userList = $('#user-list');
let messageList = $('#messages');

function drawMessage(message) {
    let position = 'left';
    const date = new Date(message.created);
    
    if (message.user.uuid === currentUser) position = 'right';
    
    const messageItem = `
        <li class="message ${position}">`
            + ( message.shop ? `<div class="avatar" style="background-image: url('${message.shop.image}'); background-size: cover;"></div>` : `<div class="avatar">${message.user.user_name}</div>`) +
                `<div class="text_wrapper">
                    <div class="text">
                        ${message.body}<br><span class="small">${date}</span>
                    </div>
                </div>
            </div>
        </li>`;
    
    $(messageItem).appendTo('#messages');
    
    if (message.product) {
        
        const messageItem = `
            <li class="message ${position}">`
                + ( message.shop ? `<div class="avatar" style="background-image: url('${message.shop.image}'); background-size: cover;"></div>` : `<div class="avatar">${message.user.user_name}</div>`) +
                    `<div class="text_wrapper" style="font-size: 10pt;">
                        <div class="row">
                            <div class="col-md-3 col-lg-3">
                                <img class="img-fluid mx-auto d-block" style="width: auto; height: auto; max-width: 100%; max-height: 100%; margin: auto; margin-top: 0px;" alt="Responsive image" src="${message.product.image}">
                            </div>
                            <div class="col-md-9 col-lg-9">
                                <div class="text">
                                    <a href="${message.product.absolute_url}">
                                        ${message.product.title}
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </li>`;
            
        $(messageItem).appendTo('#messages');
    }
}

function getConversation(recipient) {
    $.getJSON(`/chat/api/v1/message/?target=${recipient}`, function (data) {
        messageList.children('.message').remove();
        
        for (let i = data['results'].length - 1; i >= 0; i--) {
            drawMessage(data['results'][i]);
        }
        
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });
}

function getMessageById(message) {
    id = JSON.parse(message).message
    
    $.getJSON(`/chat/api/v1/message/${id}/`, function (data) {
        
        if (data.user === currentRecipient || (data.recipient === currentRecipient && data.user == currentUser)) {
            drawMessage(data);
        }
        
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });
}

function sendMessage(recipient, body) {
    $.post('/chat/api/v1/message/', {
        recipient: recipient,
        body: body
    }).done(function () {
        console.log('success send');
    }).fail(function () {
        alert('Error! Check console!');
    });
}

function setCurrentRecipient(username) {
    currentRecipient = username;
    
    getConversation(currentRecipient);
    enableInput();
}

function enableInput() {
    chatInput.prop('disabled', false);
    chatButton.prop('disabled', false);
    chatInput.focus();
}

function disableInput() {
    chatInput.prop('disabled', true);
    chatButton.prop('disabled', true);
}

$(document).ready(function () {
    
    disableInput();
    
    $('.user').click(function () {
        userList.children('.active').removeClass('active');
        let selected = event.target;
        $(selected).addClass('active');
        setCurrentRecipient(selected.id);
    });

    var socket = new WebSocket(`ws://` + window.location.host + `/ws?session_key=${sessionKey}`)

    chatInput.keypress(function (e) {
        if (e.keyCode == 13)
            chatButton.click();
    });

    chatButton.click(function () {
        if (chatInput.val().length > 0) {
            sendMessage(currentRecipient, chatInput.val());
            chatInput.val('');
        }
    });

    socket.onmessage = function (e) {
        getMessageById(e.data);
    };
});
