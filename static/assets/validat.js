const passwordField = document.getElementById('password');
const passwordValidationMsg = document.getElementById('password-validation-msg');

passwordField.addEventListener('input', () => {
  const password = passwordField.value;

  // Define password requirements
  const hasUpperCase = /[A-Z]/.test(password);
  const hasLowerCase = /[a-z]/.test(password);
  const hasNumber = /[0-9]/.test(password);
  const hasSpecialChar = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password);
  const isLongEnough = password.length >= 8;

  // Check if password meets all requirements
  if (hasUpperCase && hasLowerCase && hasNumber && hasSpecialChar && isLongEnough) {
    passwordValidationMsg.innerText = '';
    passwordField.setCustomValidity('');
  } else {
    passwordValidationMsg.innerText = 'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character.';
    passwordField.setCustomValidity('Invalid password');
  }
});