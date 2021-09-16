$(document).on('click', '#add-button', function (e) {
    e.preventDefault();
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
})
