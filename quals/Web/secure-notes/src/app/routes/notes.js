const notes = require('express').Router();
const path = require('path');
const { sanitize_notes } = require('../utils/sanitizer');
const { dbManager } = require('../utils/database');
const { convert } = require('html-to-text');

function requireAuth(req, res, next) {
    if (!req.session.user) {
        return res.redirect('/');
    }
    next();
}

function adminCantModifyNotes(req, res, next) {
    if (req.session.user.username === 'admin') {
        return res.status(403).json({ error: 'Admin can\'t modify the notes' }); 
    }
    next();
}

function databaseOrTemporary(choice){
    switch (choice) {
        case "temporary":
            return "temporary";

        case "database":
            return "database";
        default:
            return "temporary";
    }
}

notes.use(requireAuth);

notes.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../templates/notes.html'));
});

notes.get('/list', async (req, res) => {
    try {
        const username = req.session.user.username;
        // const storageType = req.query.storage || 'temporary';
        const storageType = databaseOrTemporary(req.query.storage);
        const folderId = req.query.folderId ? parseInt(req.query.folderId) : null;
        
        let userNotes;
        if (storageType === 'database') {
            const userId = await getUserId(username);
            userNotes = await dbManager.getNotesFromDatabase(userId, folderId);
        } else {
            userNotes = dbManager.getNotesFromTemporary(username, folderId);
        }
        
        res.json(userNotes);
    } catch (error) {
        console.error('Error fetching notes:', error);
        res.status(500).json({ error: 'Failed to fetch notes' });
    }
});


notes.post('/create', adminCantModifyNotes, async (req, res) => {
    try {
        const { title, content, folderId } = req.body;
        const username = req.session.user.username;
        
        if (!title || !content) {
            return res.status(400).json({ error: 'Title and content are required' });
        }
        
        if (!folderId) {
            return res.status(400).json({ error: 'Folder selection is required' });
        }
        
        const cleanTitle = sanitize_notes(title);
        const cleanContent = sanitize_notes(content);
        const userId = await getUserId(username);
        
        // Determine storage type based on folder location
        let newNote;
        let isTemporaryFolder = false;
        
        // Check if folder exists in temporary storage
        const tempFolders = dbManager.getTemporaryFolders(username);
        const tempFolder = tempFolders.find(f => f.id === parseInt(folderId));
        
        if (tempFolder) {
            // Folder is in temporary storage
            isTemporaryFolder = true;
            newNote = dbManager.saveNoteToTemporary(username, parseInt(folderId), cleanTitle, cleanContent);
        } else {
            // Check if folder exists in database storage
            const dbFolders = await dbManager.getFoldersByUser(userId);
            const dbFolder = dbFolders.find(f => f.id === parseInt(folderId));
            
            if (dbFolder) {
                // Folder is in database storage
                newNote = await dbManager.saveNoteToDatabase(userId, parseInt(folderId), cleanTitle, cleanContent);
            } else {
                return res.status(400).json({ error: 'Selected folder not found' });
            }
        }
        
        res.redirect('/note');
    } catch (error) {
        console.error('Error creating note:', error);
        res.status(500).json({ error: 'Failed to create note' });
    }
});

notes.get('/:id', async (req, res) => {
    try {
        const noteId = parseInt(req.params.id);
        const username = req.session.user.username;
        // const storageType = req.query.storage || 'temporary';
        const storageType = databaseOrTemporary(req.query.storage);
        
        let userNotes;
        if (storageType === 'database') {
            const userId = await getUserId(username);
            userNotes = await dbManager.getNotesFromDatabase(userId);
        } else {
            userNotes = dbManager.getNotesFromTemporary(username);
        }
        
        const note = userNotes.find(n => n.id === noteId);
        if (!note) {
            return res.status(404).json({ error: 'Note not found' });
        }
        
        res.json(note);
    } catch (error) {
        console.error('Error fetching note:', error);
        res.status(500).json({ error: 'Failed to fetch note' });
    }
});

notes.delete('/:id', adminCantModifyNotes, async (req, res) => {
    try {
        const noteId = parseInt(req.params.id);
        const username = req.session.user.username;
        // const storageType = req.query.storage || 'temporary';
        const storageType = databaseOrTemporary(req.query.storage);
        
        let deleted;
        if (storageType === 'database') {
            const userId = await getUserId(username);
            deleted = await dbManager.deleteNoteFromDatabase(noteId, userId);
        } else {
            deleted = dbManager.deleteNoteFromTemporary(noteId, username);
        }
        
        if (!deleted) {
            return res.status(404).json({ error: 'Note not found' });
        }
        
        res.json({ message: 'Note deleted successfully' });
    } catch (error) {
        console.error('Error deleting note:', error);
        res.status(500).json({ error: 'Failed to delete note' });
    }
});

notes.post('/search', async (req, res) => {
    try {
        const { tables, searchValue } = req.body;
        const username = req.session.user.username;
        
        if (!searchValue || searchValue.trim() === '') {
            return res.status(400).json({ error: 'Search value is required' });
        }
        
        const userId = await getUserId(username);
        const searchTables = tables || ['folders'];
        
        const searchResult = await dbManager.searchAcrossFolders(searchTables, userId, searchValue.trim(), username);
        
        res.json(searchResult);
        
    } catch (error) {
        console.error('Search endpoint error:', error);
        res.status(500).json({ 
            error: 'Search failed',
            details: error.message 
        });
    }
});

// Export single note as text file
notes.get('/export/:id', async (req, res) => {
    try {
        const noteId = parseInt(req.params.id);
        const username = req.session.user.username;
        // const storageType = req.query.storage || 'temporary';
        const storageType = databaseOrTemporary(req.query.storage);
        
        let note = null;
        
        // Find note in appropriate storage
        if (storageType === 'database') {
            const userId = await getUserId(username);
            const userNotes = await dbManager.getNotesFromDatabase(userId);
            note = userNotes.find(n => n.id === noteId);
        } else {
            const userNotes = dbManager.getNotesFromTemporary(username);
            note = userNotes.find(n => n.id === noteId);
        }
        
        if (!note) {
            return res.status(404).json({ error: 'Note not found' });
        }
        
        // Convert HTML content to clean text
        const textContent = convert(note.content, {
            wordwrap: 80,
            preserveNewlines: true,
        });
        
        // Create filename (sanitize for file system)
        const filename = `${noteId}.txt`;
        
        // Set response headers for file download
        res.setHeader('Content-Disposition', `inline; filename="${filename}"`);
        
        // Send formatted content
        const exportContent = `Title: ${note.title}\nCreated: ${new Date(note.createdAt).toLocaleString()}\nStorage: ${storageType}\n\n${textContent}`;
        res.send(exportContent);
        
    } catch (error) {
        console.error('Error exporting note:', error);
        res.status(500).json({ error: 'Failed to export note' });
    }
});

async function getUserId(username) {
    return await dbManager.getUserIdFromDatabase(username);
}

module.exports = notes;