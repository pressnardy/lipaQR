
function validate_tables_input(inputId) {
    const input = document.getElementById(inputId);
    if(!input){return}
    input.addEventListener('input', () => {
        const value = input.value;
        const isValid = /^[1-9]\d*$/.test(value);

        if (!isValid && value !== '') {
        input.setCustomValidity('Please enter a positive non-zero integer');
        input.reportValidity();
        } else {
        input.setCustomValidity('');
        }
    });
}


validate_tables_input('tables');

// function setTableNumber() {
//     const form = document.getElementById('table-number-form')
//     if(!form) {
//         return
//     }
//     const tableNumber = form.querySelector('#table-number')?.value
//     const createOrder = form.querySelector('#create-order')
//     createOrder.addEventListener('click', (e)=> {
//         e.preventDefault()
//         console.log(form.action)
//     })
// }

// setTableNumber()