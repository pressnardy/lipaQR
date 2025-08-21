
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


async function fetchAndUpdate() {
  try {
    const response = await fetch(newDataUrl);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    updateAlerts(data);
  } catch (error) {
    console.error('Fetch error:', error);
  }
}

fetchAndUpdate()

setInterval(fetchAndUpdate, 30000);
