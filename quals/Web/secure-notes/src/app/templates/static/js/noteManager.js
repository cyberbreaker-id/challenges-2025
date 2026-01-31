// Note Management Module
class NoteManager {
    constructor() {
        this.notesCache = { temporary: [], database: [] };
    }

    databaseOrTemporary(choice) {
        switch (choice) {
            case "temporary":
                return "temporary";

            case "database":
                return "database";

            default:
                return "temporary";
        }
    }

    async loadNotesForFolder(folderId) {
        try {
            folderId = parseInt(folderId);
            currentStorageType = this.databaseOrTemporary(currentStorageType);
            const response = await fetch(`/note/list?storage=${currentStorageType}&folderId=${folderId}`);
            const notesRaw = await response.json();
            
            const notes = notesRaw.map(item => {
                if (item.notes) return item.notes;
                return item;
            });
            
            const notesList = document.getElementById('notesList');
            notesList.innerHTML = '';
            
            if (notes.length === 0) {
                notesList.innerHTML = '<div class="note-card"><p>No notes in this folder.</p></div>';
            } else {
                notes.forEach(note => {
                    const noteCard = document.createElement('div');
                    noteCard.className = 'note-card';
                    noteCard.innerHTML = `
                        <div class="note-actions">
                            <button class="btn btn-small btn-primary" onclick="noteManager.exportNote(${note.id}, '${currentStorageType}')">Export</button>
                            <button class="btn btn-small btn-danger" onclick="noteManager.deleteNote(${note.id}, '${currentStorageType}')">Delete</button>
                        </div>
                        <div class="note-title">${escapeHtml(note.title)}</div>
                        <div class="note-content">${escapeHtml(note.content)}</div>
                        <div class="note-meta">
                            <span>Created: ${escapeHtml(formatDate(note.createdAt))}</span>
                            <span class="private-badge">Storage: ${currentStorageType === 'temporary' ? 'Temporary' : 'Database'}</span>
                        </div>
                    `;
                    notesList.appendChild(noteCard);
                });
            }
            
            // Update note count
            this.updateNoteCount();
        } catch (error) {
            console.error('Error loading notes:', error);
        }
    }

    async exportNote(noteId, storageType) {
        try {
            // Create a temporary link to trigger download
            noteId = parseInt(noteId);
            const link = document.createElement('a');
            link.href = `/note/export/${noteId}?storage=${storageType}`;
            link.download = '';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } catch (error) {
            console.error('Error exporting note:', error);
            alert('Error exporting note');
        }
    }

    async deleteNote(noteId, storageType) {
        if (confirm('Are you sure you want to delete this note?')) {
            try {
                const response = await fetch(`/note/${noteId}?storage=${storageType}`, {
                    method: 'DELETE'
                });
                
                if (response.ok) {
                    // Reload notes for current folder
                    if (folderManager.selectedFolderId) {
                        await this.loadNotesForFolder(folderManager.selectedFolderId);
                    }
                } else {
                    const errorData = await response.json();
                    alert(errorData.error || 'Error deleting note');
                }
            } catch (error) {
                console.error('Error deleting note:', error);
                alert('Error deleting note');
            }
        }
    }

    updateNoteCount() {
        // This would need to be updated to count notes across all folders
        document.getElementById('noteCount').textContent = '';
    }
}

// Initialize note manager
const noteManager = new NoteManager();