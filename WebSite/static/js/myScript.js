$('.plus-cart').click(function () {
    var id = $(this).attr('pid').toString()
    var qyantity = this.parentNode.children[2]

    $.ajax({
        type: 'GET',
        url: '/pluscart',
        data: {
            cart_id: id
        },

        success: function (data) {
            console.log(data)
            qyantity.innerText = data.qyantity
            document.getElementById(`qyantity${id}`).innerText = data.qyantity
            document.getElementById('amount_tt').innerText = data.amount
            document.getElementById('totalamount').innerText = data.total

        }
    })
})


$('.minus-cart').click(function () {
    var id = $(this).attr('pid').toString()
    var qyantity = this.parentNode.children[2]

    $.ajax({
        type: 'GET',
        url: '/minuscart',
        data: {
            cart_id: id
        },

        success: function (data) {
            console.log(data)
            qyantity.innerText = data.qyantity
            document.getElementById(`qyantity${id}`).innerText = data.qyantity
            document.getElementById('amount_tt').innerText = data.amount
            document.getElementById('totalamount').innerText = data.total

        }
    })
})


$('.remove-cart').click(function () {
    var id = $(this).attr('pid').toString()
    var to_remove = this.parentNode.parentNode.parentNode.parentNode

    $.ajax({
        type: 'GET',
        url: '/removecart',
        data: {
            cart_id: id
        },
        success: function (data) {
            document.getElementById('amount_tt').innerText = data.amount
            document.getElementById('totalamount').innerText = data.total
            to_remove.remove()
        }
    })
})
