// Delete Item
$(document).on('click', '.delete-button', function (e) {
    e.preventDefault();
    var prodid = $(this).data('index');
    $.ajax({
        type: 'POST',
        url: urlCartDelete,
        data: {
            productid: $(this).data('index'),
            csrfmiddlewaretoken: csrfToken,
            action: 'post'
        },
        success: function (json) {
            $('.product-item[data-index="' + prodid + '"]').remove();
            document.getElementById("subtotal").innerHTML = json.subtotal;
            document.getElementById("cart-qty").innerHTML = json.qty
        },
        error: function (xhr, errmsg, err) {}
    });
})

// Update Item
$(document).on('click', '.update-button', function (e) {
    e.preventDefault();
    var prodid = $(this).data('index');
    $.ajax({
        type: 'POST',
        url: urlCartUpdate,
        data: {
            productid: $(this).data('index'),
            productqty: $('#select' + prodid + ' option:selected').text(),
            csrfmiddlewaretoken: csrfToken,
            action: 'post'
        },
        success: function (json) {
            document.getElementById("cart-qty").innerHTML = json.qty
            document.getElementById("subtotal").innerHTML = json.subtotal
        },
        error: function (xhr, errmsg, err) {}
    });
})

function increase(id) {
    var qty = parseInt(document.getElementById('item-qty-' + id).innerHTML)
    var price = Number(document.getElementById('item-price-' + id).innerHTML.replace(/[^0-9.-]+/g,""))
    
    qty = qty >= 4 ? 4 : qty + 1
    
    $.ajax({
        type: 'POST',
        url: urlCartUpdate,
        data: {
            productid: id,
            productqty: qty,
            csrfmiddlewaretoken: csrfToken,
            action: 'post'
        },
        success: function (json) {
            document.getElementById('item-qty-' + id).innerHTML = qty
            document.getElementById('item-total-' + id).innerHTML = (new Intl.NumberFormat('id-ID').format(price * qty)).split(".").join(",") + '.0'
            
            document.getElementById("cart-qty").innerHTML = json.qty
            document.getElementById("subtotal").innerHTML = (new Intl.NumberFormat('id-ID').format(json.subtotal)).split(".").join(",") + '.0'
        },
        error: function (xhr, errmsg, err) {}
    });
}

function decrease(id) {
    var qty = parseInt(document.getElementById('item-qty-' + id).innerHTML)
    var price = Number(document.getElementById('item-price-' + id).innerHTML.replace(/[^0-9.-]+/g,""))
    
    qty = qty == 1 ? qty : qty - 1
    $.ajax({
        type: 'POST',
        url: urlCartUpdate,
        data: {
            productid: id,
            productqty: qty,
            csrfmiddlewaretoken: csrfToken,
            action: 'post'
        },
        success: function (json) {
            document.getElementById('item-qty-' + id).innerHTML = qty
            document.getElementById('item-total-' + id).innerHTML = (new Intl.NumberFormat('id-ID').format(price * qty)).split(".").join(",") + '.0'
            
            document.getElementById("cart-qty").innerHTML = json.qty
            document.getElementById("subtotal").innerHTML = (new Intl.NumberFormat('id-ID').format(json.subtotal)).split(".").join(",") + '.0'
        },
        error: function (xhr, errmsg, err) {}
    });
}
