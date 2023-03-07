const addBtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < addBtns.length; i++) {
    addBtns[i].addEventListener('click', function () {
        let productId = this.dataset.product
        let action = this.dataset.action

        if (user == 'AnonymousUser') {
            alert('Login is required')
        }
        else {
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action) {
    const url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
        .then(response =>  response.json())
        .then(data => {
            location.reload()
        })
}