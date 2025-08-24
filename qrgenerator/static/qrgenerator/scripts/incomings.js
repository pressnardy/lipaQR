
const newDataUrl = document.getElementById('incoming-url').href;
const paidContainer = document.getElementById('incoming-paid');
const pendingContainer = document.getElementById('incoming-pending');

console.log(newDataUrl)

function updateAlerts(data) {
    if(data.paid) {
        paidContainer.textContent = data.paid
    }
    if(data.pending) {
        pendingContainer.innerText = data.pending
    }
}


function getOrderElement(order) {
  const orderHTML = `
      <a href="/orders/${order.id}/">
        <div class="element-highlight is-new">
            <svg width="16px" height="16px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="#663399" stroke-width="0.36" transform="rotate(0)">
                <path d="M9.39862 4.32752C9.69152 4.03463 10.1664 4.03463 10.4593 4.32752L16.8232 10.6915C17.5067 11.3749 17.5067 12.4829 16.8232 13.1664L10.4593 19.5303C10.1664 19.8232 9.69152 19.8232 9.39863 19.5303C9.10573 19.2374 9.10573 18.7625 9.39863 18.4697L15.7626 12.1057C15.8602 12.0081 15.8602 11.8498 15.7626 11.7521L9.39863 5.38818C9.10573 5.09529 9.10573 4.62041 9.39862 4.32752Z" fill="rebeccapurple"></path>
            </svg>
            <span class="item-name item-property">
            ${order.phoneNumber} | KES: ${order.totalAmount}  
            </span>
        </div>
        </a>
    `
  const div = document.createElement('div')
  div.innerHTML = orderHTML.trim()
  console.log(div.firstChild)
  return div.firstChild
}

function getViewOrderURL() {
  const url = document.getElementById('view-order-url')?.href
  return url
}

function updateIncomings(data) {
  const container = document.getElementById('incomings-container')
  if(!container){
    return
  }
  container.innerHTML = ""
  const incomingOrders = data.all
  incomingOrders.forEach(order => {
    const orderHTML = getOrderElement(order)
    container.appendChild(orderHTML)
    
  });
}


async function fetchAndUpdate() {
  try {
    const response = await fetch(newDataUrl);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    updateAlerts(data);
    updateIncomings(data)
    
  } catch (error) {
    console.error('Fetch error:', error);
  }
}


fetchAndUpdate()

setInterval(fetchAndUpdate, 30000);
