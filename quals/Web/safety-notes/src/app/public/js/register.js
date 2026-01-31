document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const submitButton = document.querySelector('button[type="submit"]');
    const usernameInput = document.querySelector('input[name="username"]');
    const passwordInput = document.querySelector('input[name="password"]');
    
    // Password strength indicator
    function createPasswordStrengthIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'password-strength';
        indicator.innerHTML = `
            <div class="strength-bar">
                <div class="strength-fill"></div>
            </div>
            <div class="strength-text">Password strength</div>
        `;
        passwordInput.parentNode.appendChild(indicator);
        return indicator;
    }
    
    const strengthIndicator = createPasswordStrengthIndicator();
    const strengthFill = strengthIndicator.querySelector('.strength-fill');
    const strengthText = strengthIndicator.querySelector('.strength-text');
    
    // Check password strength
    function checkPasswordStrength(password) {
        let score = 0;
        let feedback = [];
        
        if (password.length >= 8) score++;
        else feedback.push('at least 8 characters');
        
        if (/[a-z]/.test(password)) score++;
        else feedback.push('lowercase letter');
        
        if (/[A-Z]/.test(password)) score++;
        else feedback.push('uppercase letter');
        
        if (/[0-9]/.test(password)) score++;
        else feedback.push('number');
        
        if (/[^A-Za-z0-9]/.test(password)) score++;
        else feedback.push('special character');
        
        return { score, feedback };
    }
    
    // Update password strength indicator
    function updatePasswordStrength() {
        const password = passwordInput.value;
        const { score, feedback } = checkPasswordStrength(password);
        
        const percentage = (score / 5) * 100;
        strengthFill.style.width = percentage + '%';
        
        if (score === 0) {
            strengthFill.style.backgroundColor = '#ccc';
            strengthText.textContent = 'Password strength';
        } else if (score <= 2) {
            strengthFill.style.backgroundColor = '#ff4444';
            strengthText.textContent = 'Weak password';
        } else if (score <= 3) {
            strengthFill.style.backgroundColor = '#ffaa00';
            strengthText.textContent = 'Medium password';
        } else if (score <= 4) {
            strengthFill.style.backgroundColor = '#88cc00';
            strengthText.textContent = 'Strong password';
        } else {
            strengthFill.style.backgroundColor = '#00aa00';
            strengthText.textContent = 'Very strong password';
        }
        
        if (feedback.length > 0) {
            strengthText.textContent += ' (needs: ' + feedback.join(', ') + ')';
        }
    }
    
    // Form validation
    function validateForm() {
        const username = usernameInput.value.trim();
        const password = passwordInput.value;
        
        if (username.length < 3) {
            showError('Username must be at least 3 characters long');
            return false;
        }
        
        if (!/^[a-zA-Z0-9_]+$/.test(username)) {
            showError('Username can only contain letters, numbers, and underscores');
            return false;
        }
        
        const { score } = checkPasswordStrength(password);
        if (score < 3) {
            showError('Password is too weak. Please choose a stronger password.');
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
        submitButton.textContent = 'Creating account...';
    });
    
    // Real-time validation feedback
    usernameInput.addEventListener('input', function() {
        const username = this.value.trim();
        if (username.length >= 3 && /^[a-zA-Z0-9_]+$/.test(username)) {
            this.style.borderColor = '#4CAF50';
        } else {
            this.style.borderColor = '';
        }
    });
    
    passwordInput.addEventListener('input', updatePasswordStrength);
});