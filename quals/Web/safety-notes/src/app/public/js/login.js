document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const submitButton = document.querySelector('button[type="submit"]');
    const usernameInput = document.querySelector('input[name="username"]');
    const passwordInput = document.querySelector('input[name="password"]');
    
    // Form validation
    function validateForm() {
        const username = usernameInput.value.trim();
        const password = passwordInput.value;
        
        if (username.length < 3) {
            showError('Username must be at least 3 characters long');
            return false;
        }
        
        if (password.length < 6) {
            showError('Password must be at least 6 characters long');
            return false;
        }
        
        return true;
    }
    
    // Show error message
    function showError(message) {
        const existingError = document.querySelector('.js-error');
        if (existingError) {
            existingError.remove();
        }
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error js-error';
        errorDiv.textContent = message;
        form.insertBefore(errorDiv, form.firstChild);
        
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }
    
    // Form submission
    form.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
            return;
        }
        
        submitButton.disabled = true;
        submitButton.textContent = 'Logging in...';
    });
    
    // Real-time validation feedback
    usernameInput.addEventListener('input', function() {
        if (this.value.length >= 3) {
            this.style.borderColor = '#4CAF50';
        } else {
            this.style.borderColor = '';
        }
    });
    
    passwordInput.addEventListener('input', function() {
        if (this.value.length >= 6) {
            this.style.borderColor = '#4CAF50';
        } else {
            this.style.borderColor = '';
        }
    });
});