const form = document.querySelector('.login-form');
const emailInput = document.querySelector('input[type="email"]');
const passwordInput = document.querySelector('input[type="password"]');

form.addEventListener('submit', (e) => {
  e.preventDefault();
  
  if (!emailInput.value) {
    showError(emailInput, 'Email is required');
  } else {
    showSuccess(emailInput);
  }

  if (!passwordInput.value) {
    showError(passwordInput, 'Password is required');
  } else {
    showSuccess(passwordInput);
  }
});

function showError(input, message) {
  const formGroup = input.parentElement;
  formGroup.classList.remove('success');
  formGroup.classList.add('error');
  const error = formGroup.querySelector('.error-message') || document.createElement('div');
  error.className = 'error-message';
  error.textContent = message;
  if (!formGroup.querySelector('.error-message')) {
    formGroup.appendChild(error);
  }
  formGroup.classList.add('shake');
  setTimeout(() => formGroup.classList.remove('shake'), 500);
}

function showSuccess(input) {
  const formGroup = input.parentElement;
  formGroup.classList.remove('error');
  formGroup.classList.add('success');
  const error = formGroup.querySelector('.error-message');
  if (error) {
    formGroup.removeChild(error);
  }
}