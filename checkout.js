document.addEventListener('DOMContentLoaded', function() {
    const paymentMethodSelect = document.getElementById('payment-method');
    const cardDetailsContainer = document.getElementById('card-details-container');
    const upiDetailsContainer = document.getElementById('upi-details-container');
    const checkoutForm = document.getElementById('checkout-form');

    paymentMethodSelect.addEventListener('change', function () {
        if (paymentMethodSelect.value === 'credit-card' || paymentMethodSelect.value === 'debit-card') {
            cardDetailsContainer.style.display = 'flex';
            upiDetailsContainer.style.display = 'none';
        } else if (paymentMethodSelect.value === 'upi') {
            cardDetailsContainer.style.display = 'none';
            upiDetailsContainer.style.display = 'flex';
        } else {
            cardDetailsContainer.style.display = 'none';
            upiDetailsContainer.style.display = 'none';
        }
    });

    checkoutForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the form from submitting the default way
        window.location.href = '{{ url_for("order_confirmation") }}'; // Redirect to the Order Confirmation page
    });
});