let chatInput = $('#chat-input');
var messageList = $('#messages');

function addCart() {
    $.ajax({
        type: 'POST',
        url: urlCartAdd,
        data: {
            productid: $('#add-button').val(),
            productqty: $('#select option:selected').text(),
            csrfmiddlewaretoken: csrfToken,
            action: 'post'
        },
        success: function (json) {
            document.getElementById("cart-qty").innerHTML = json.qty
        },
        error: function (xhr, errmsg, err) {}
    });
}

function drawMessage(message) {
    let position = 'left';
    const date = new Date(message.created);
    
    if (message.user === currentUser) position = 'right';
    
    const messageItem = `
        <li class="message ${position}">
            <div class="text_wrapper" style="margin-right: 0px; margin-left: 0px; padding: 10px;">
                    ${message.body}
                </div>
            </div>
        </li>`;
    
    $(messageItem).appendTo('#messages');
    
    if (message.product) {
        
        const messageItem = `
            <li class="message ${position}">
                <div class="text_wrapper" style="margin-right: 0px; margin-left: 0px; padding: 10px;">
                    <div class="row">
                        <div class="col-md-3 col-lg-3">
                            <img class="img-fluid mx-auto d-block" style="width: auto; height: auto; max-width: 100%; max-height: 100%; margin: auto; margin-top: 0px;" alt="Responsive image" src="${message.product.image}">
                        </div>
                        <div class="col-md-9 col-lg-9">
                            <a href="${message.product.absolute_url}">
                                ${message.product.title}
                            </a>
                        </div>
                    </div>
                </div>
            </li>`;
    
        $(messageItem).appendTo('#messages');
    }
}

function getMessages() {
    $.getJSON(`/chat/api/v1/message/?target=${currentRecipient}`, function (data) {
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

function sendMessage(body) {
    $.post('/chat/api/v1/message/', {
        recipient: currentRecipient,
        body: body,
        slug: document.getElementById('product') != null ? document.getElementById('product').value : '',
    }).done(function () {
        console.log('success send');
    }).fail(function () {
        alert('Error! Check console!');
    });
    if (document.getElementById('product') != null) closeProduct()
}

function openChat() {
    document.getElementById("chat-box").style.display = 'block'
    $( "#send-message").focus();
}

function closeChat() {
    document.getElementById("chat-box").style.display = 'none'
}

function closeProduct() {
    document.getElementById("chat-message-product").remove()
}

$(document).ready(function () {
    $('#add-button').click(function () {
        addCart()
    })
    
    $('#chat-button').click(function () {
        getMessages()
        openChat()
    })
    
    chatInput.keypress(function (e) {
        if (e.keyCode == 13) {
            sendMessage(chatInput.val());
            chatInput.val('');
        }
    });
    
    var socket = new WebSocket(`ws://` + window.location.host + `/ws?session_key=${sessionKey}`)
    
    socket.onmessage = function (e) {
        getMessageById(e.data);
    };
})
