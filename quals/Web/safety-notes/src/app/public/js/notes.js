document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const titleInput = document.querySelector('input[name="title"]');
    const contentTextarea = document.querySelector('textarea[name="content"]');
    const submitButton = document.querySelector('button[type="submit"]');
    const notesGrid = document.querySelector('.notes-grid');
    
    // Character counter for title and content
    function createCharCounter(element, maxLength) {
        const counter = document.createElement('div');
        counter.className = 'char-counter';
        counter.style.cssText = 'text-align: right; font-size: 12px; color: #666; margin-top: 5px;';
        element.parentNode.appendChild(counter);
        
        function updateCounter() {
            const remaining = maxLength - element.value.length;
            counter.textContent = `${element.value.length}/${maxLength} characters`;
            
            if (remaining < 20) {
                counter.style.color = '#ff4444';
            } else if (remaining < 50) {
                counter.style.color = '#ffaa00';
            } else {
                counter.style.color = '#666';
            }
        }
        
        element.addEventListener('input', updateCounter);
        updateCounter();
        
        return counter;
    }
    
    // Add character counters
    createCharCounter(titleInput, 100);
    createCharCounter(contentTextarea, 1000);
    
    // Auto-resize textarea
    function autoResizeTextarea() {
        contentTextarea.style.height = 'auto';
        contentTextarea.style.height = contentTextarea.scrollHeight + 'px';
    }
    
    contentTextarea.addEventListener('input', autoResizeTextarea);
    autoResizeTextarea();
    
    // Form validation
    function validateForm() {
        const title = titleInput.value.trim();
        const content = contentTextarea.value.trim();
        
        if (title.length === 0) {
            showError('Title is required');
            titleInput.focus();
            return false;
        }
        
        if (title.length > 100) {
            showError('Title must be 100 characters or less');
            titleInput.focus();
            return false;
        }
        
        if (content.length === 0) {
            showError('Content is required');
            contentTextarea.focus();
            return false;
        }
        
        if (content.length > 1000) {
            showError('Content must be 1000 characters or less');
            contentTextarea.focus();
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
        errorDiv.style.cssText = 'background: #ff4444; color: white; padding: 10px; border-radius: 4px; margin-bottom: 15px;';
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
        submitButton.textContent = 'Adding Note...';
    });
    
    // Enhanced delete confirmation
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const noteTitle = this.closest('.note').querySelector('h3').textContent;
            const confirmMsg = `Are you sure you want to delete the note "${noteTitle}"? This action cannot be undone.`;
            
            if (confirm(confirmMsg)) {
                // Show loading state
                this.textContent = 'Deleting...';
                this.style.pointerEvents = 'none';
                
                // Navigate to delete URL
                window.location.href = this.href;
            }
        });
    });
    
    form.addEventListener('submit', function() {
    });
    
});