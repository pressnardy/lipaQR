
const addButtons = document.querySelectorAll('.add-button');
addButtons.forEach(button => {
    button.addEventListener('click', function() {
        const parent = this.parentElement;
        const input = parent.querySelector('input');

        input.value = (Number(input.value) + 1).toString();
        setTotal()
    });
})

const reduceButtons = document.querySelectorAll('.reduce-button');
reduceButtons.forEach(button => {
    button.addEventListener('click', function() {
        const parent = this.parentElement;
        const input = parent.querySelector('input');

        if (Number(input.value) > 0) {
            input.value = (Number(input.value) - 1).toString();
            setTotal()
        }
    });
})

function setTotal() {
    const orderItems = document.querySelectorAll('.order-item')
    orderItems.forEach(item => {
        const itemId = item.id
        const itemPrice = item.querySelector(`#${itemId}-price`)?.innerText || null
        // console.log(itemId)
        if (!itemPrice){
            console.error(`#${itemId}-price not found`)
        }
        const itemQuantity = item.querySelector(`#${itemId}-quantity`)?.value
        const totalElement = item.querySelector(`#${itemId}-total`) || null;
        if (!totalElement) {
            console.error(`#${itemId}-total not found`)
        }
        totalElement.innerText = (Number(itemQuantity) * itemPrice).toString();
        // console.log(totalElement.innerText)
    })
}

function setMenuTotal () {

}
