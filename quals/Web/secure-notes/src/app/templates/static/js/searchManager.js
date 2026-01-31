// Search Management Module
class SearchManager {
    constructor() {
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Add Enter key support for search
        document.addEventListener('DOMContentLoaded', () => {
            const searchInput = document.getElementById('searchInput');
            if (searchInput) {
                searchInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        this.performSearch();
                    }
                });
            }
        });
    }

    async performSearch() {
        const searchValue = document.getElementById('searchInput').value.trim();
        
        if (!searchValue) {
            alert('Please enter a search term');
            return;
        }
        
        try {
            const response = await fetch('/note/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ searchValue })
            });
            
            const searchResult = await response.json();
            
            if (searchResult.success) {
                this.displaySearchResults(searchResult);
            } else {
                alert(searchResult.error || 'Search failed');
            }
        } catch (error) {
            console.error('Search error:', error);
            alert('Search failed');
        }
    }

    displaySearchResults(searchResult) {
        const notesList = document.getElementById('notesList');
        notesList.innerHTML = '';
        
        if (searchResult.results.length === 0) {
            notesList.innerHTML = '<div class="note-card"><p>No notes found for your search.</p></div>';
        } else {
            const searchHeader = document.createElement('div');
            searchHeader.className = 'note-card';
            searchHeader.style.backgroundColor = '#e3f2fd';
            searchHeader.innerHTML = `
                <h4>Search Results (${escapeHtml(searchResult.results.length)} found)</h4>
                <p>Searched for: "${escapeHtml(searchResult.searchValue)}" across folders</p>
            `;
            notesList.appendChild(searchHeader);
            
            searchResult.results.forEach(note => {
                const noteCard = document.createElement('div');
                noteCard.className = 'note-card';
                noteCard.innerHTML = `
                    <div class="note-title">${escapeHtml(note.title)}</div>
                    <div class="note-content">${escapeHtml(note.content)}</div>
                    <div class="note-meta">
                        <span>Created: ${escapeHtml(formatDate(note.createdAt))}</span>
                        <span class="private-badge">Folder: ${escapeHtml(note.folderName) || 'Unknown'}</span>
                    </div>
                `;
                notesList.appendChild(noteCard);
            });
        }
        
        // Clear folder selection
        document.querySelectorAll('.folder-card').forEach(card => card.classList.remove('selected'));
        folderManager.selectedFolderId = null;
        document.getElementById('selectedFolderId').value = '';
        document.getElementById('folderSelection').textContent = 'Select a folder above to continue';
        document.getElementById('createBtn').disabled = true;
    }

    clearSearch() {
        document.getElementById('searchInput').value = '';
        document.getElementById('notesList').innerHTML = '';
        
        // Reload folder selection
        const firstFolder = document.querySelector('.folder-card');
        if (firstFolder) {
            firstFolder.click();
        }
    }
}

// Initialize search manager
const searchManager = new SearchManager();