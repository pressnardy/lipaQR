
function filterOrders(selectId='orders-select') {
    const selectElement = document.getElementById(selectId);
    if (!selectElement) {
        console.warn(`Select element with ID '${selectId}' not found.`);
        return;
    }
    selectElement.addEventListener('change', () => {
    const form = selectElement.closest('form');
    if (form) {form.submit();} 
    else {
        console.warn('No parent form found for the select element.');
    }
    });
}

filterOrders()


