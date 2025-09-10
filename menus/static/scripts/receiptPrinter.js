// Import libraries from CDN
import ReceiptPrinterEncoder from 'https://cdn.jsdelivr.net/npm/receipt-printer-encoder/dist/receipt-printer-encoder.esm.js';
import WebSerialReceiptPrinter from 'https://cdn.jsdelivr.net/npm/@point-of-sale/webserial-receipt-printer/dist/webserial-receipt-printer.esm.js';

/**
 * Prints a restaurant receipt using Web Serial API
 * @param {string} restaurantName - Name of the restaurant
 * @param {string} orderId - Unique order ID
 * @param {string} tableNumber - Table number
 * @param {Array<{ name: string, total: number }>} items - List of items
 */
export async function printReceipt(restaurantName, orderId, tableNumber, items) {
  const encoder = new ReceiptPrinterEncoder();
  encoder.initialize();
  encoder.setCharacterCodeTable(0); // Default code page
  encoder.setTextSize(1, 1);
  encoder.setTextAlign('center');
  encoder.text(restaurantName.toUpperCase());
  encoder.newline();

  encoder.setTextSize(0, 0);
  encoder.setTextAlign('left');
  encoder.text(`Order ID: ${orderId}`);
  encoder.text(`Table No: ${tableNumber}`);
  encoder.newline();

  encoder.text('------------------------------');
  items.forEach(item => {
    const name = item.name.padEnd(24, ' ');
    const price = item.total.toFixed(2).padStart(6, ' ');
    encoder.text(`${name}${price}`);
  });

  encoder.text('------------------------------');

  const total = items.reduce((sum, item) => sum + item.total, 0);
  encoder.setTextAlign('right');
  encoder.text(`TOTAL: ${total.toFixed(2)}`);
  encoder.newline();

  encoder.setTextAlign('center');
  encoder.text('Thank you!');
  encoder.newline();
  encoder.cut();

  const data = encoder.encode();

  const printer = new WebSerialReceiptPrinter({ baudRate: 9600 });
  await printer.connect(); // Must be triggered by user gesture
  await printer.print(data);
}


async function fetchOrder(printOrderUrl) {
    const url = printOrderUrl;
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Order not found');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching order:', error);
        return null;
    }
}


const printButtons = document.querySelectorAll('.print-order')
printButtons.forEach(button => {
  button.addEventListener('click', async () => {
    const orderUrl = document.getElementById('print-order-url')
    const data = await fetchOrder(orderUrl)
    printReceipt(data.restaurantName, data.orderId, data.tableNumber, data.items);
  })
})

