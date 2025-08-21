
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
