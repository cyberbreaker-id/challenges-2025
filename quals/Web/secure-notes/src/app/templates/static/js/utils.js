// Utility Functions
// Load saved storage type or default to temporary
let currentStorageType = localStorage.getItem('selectedStorageType') || 'temporary';

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateValue) {
    if (!dateValue) return 'Unknown';
    
    try {
        let date;
        if (dateValue instanceof Date) {
            date = dateValue;
        } else if (typeof dateValue === 'string') {
            date = new Date(dateValue);
        } else if (typeof dateValue === 'object' && dateValue.toString) {
            date = new Date(dateValue.toString());
        } else {
            return 'Unknown';
        }
        
        if (isNaN(date.getTime())) {
            return 'Unknown';
        }
        
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    } catch (error) {
        console.error('Date formatting error:', error, 'for value:', dateValue);
        return 'Unknown';
    }
}

// Global functions that need to be accessible from HTML
function switchStorage() {
    folderManager.switchStorage();
}

function showCreateFolderModal() {
    folderManager.showCreateFolderModal();
}

function closeFolderModal() {
    folderManager.closeFolderModal();
}

function performSearch() {
    searchManager.performSearch();
}

function clearSearch() {
    searchManager.clearSearch();
}

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', async () => {
    // Restore selected storage type in dropdown
    document.getElementById('viewStorageType').value = currentStorageType;
    
    // Set folder creation checkbox to match current storage type
    document.getElementById('folderIsTemporary').checked = currentStorageType === 'temporary';
    
    // Load folders for the saved storage type
    await folderManager.loadFolders(currentStorageType);
    
    // Auto-select first folder if available
    const firstFolder = document.querySelector('.folder-card');
    if (firstFolder) {
        firstFolder.click();
    }
    
    // Setup folder form submission
    document.getElementById('folderForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const folderData = {
            name: formData.get('folderName'),
            isTemporary: formData.get('folderIsTemporary')
        };
        
        await folderManager.createFolder(folderData);
    });
});