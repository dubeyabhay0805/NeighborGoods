document.addEventListener('DOMContentLoaded', function() {
    // Generate a random order number
    const orderNumber = Math.floor(100000 + Math.random() * 900000);
    document.getElementById('orderNumber').textContent = orderNumber;

    // Set the current date
    const currentDate = new Date().toLocaleDateString();
    document.getElementById('orderDate').textContent = currentDate;

    // Retrieve order details from localStorage (you'll need to set this in the checkout process)
    const orderItems = JSON.parse(localStorage.getItem('orderItems')) || [];
    const orderTotal = localStorage.getItem('orderTotal') || '0.00';
    const shippingAddress = localStorage.getItem('shippingAddress') || 'No address provided';

    // Populate order items
    const orderItemsList = document.getElementById('orderItems');
    orderItems.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.name} x ${item.quantity} - ₹${item.price * item.quantity}`;
        orderItemsList.appendChild(li);
    });

    // Set order total
    document.getElementById('orderTotal').textContent = `₹${orderTotal}`;

    // Set shipping address
    document.getElementById('shippingAddress').textContent = shippingAddress;

    // Clear localStorage after displaying the information
    localStorage.removeItem('orderItems');
    localStorage.removeItem('orderTotal');
    localStorage.removeItem('shippingAddress');
});