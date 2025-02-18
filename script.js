// Cart Management
let cartItems = [];

function addToCart(product, price) {
    cartItems.push({ product, price });
    updateCartCount();
    // You might want to send this information to the server
    // using AJAX to update the user's cart in the database
}

function updateCartCount() {
    const cartCount = document.getElementById('cart-count');
    if (cartCount) {
        cartCount.textContent = cartItems.length;
    }
}

// Search functionality
const searchForm = document.querySelector('.search-bar form');
if (searchForm) {
    searchForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const query = this.querySelector('input[name="query"]').value;
        window.location.href = `/search?query=${encodeURIComponent(query)}`;
    });
}

// Flash message dismissal
const flashMessages = document.querySelectorAll('.flash-message');
flashMessages.forEach(message => {
    message.addEventListener('click', function() {
        this.style.display = 'none';
    });
});

// Add more JavaScript functionality as needed