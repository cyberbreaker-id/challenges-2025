const { pool } = require('./connection');
const { normalizeResult } = require('./helpers');

class NoteManager {
    async saveNoteToDatabase(userId, folderId, title, content) {
        let conn;
        try {
            conn = await pool.getConnection();
            
            const result = await conn.query(
                'INSERT INTO notes (user_id, folder_id, title, content) VALUES (?, ?, ?, ?)',
                [userId, folderId, title, content]
            );
            return { id: result.insertId, userId, folderId, title, content, createdAt: new Date() };
        } catch (err) {
            console.error('Database error:', err);
            throw err;
        } finally {
            if (conn) conn.release();
        }
    }

    async getNotesFromDatabase(userId, folderId = null) {
        let conn;
        try {
            conn = await pool.getConnection();
            let query = `
                SELECT n.note_id as id, n.title, n.content, 
                       n.created_at as createdAt, n.folder_id as folderId,
                       f.folder_name as folderName
                FROM notes n 
                LEFT JOIN folders f ON n.folder_id = f.folder_id 
                WHERE n.user_id = ?
            `;
            let params = [userId];
            
            if (folderId) {
                query += ' AND n.folder_id = ?';
                params.push(folderId);
            }
            
            query += ' ORDER BY n.created_at DESC';
            
            const rows = await conn.query(query, params);
            return normalizeResult(rows);
        } catch (err) {
            console.error('Database error:', err);
            return [];
        } finally {
            if (conn) conn.release();
        }
    }

    async deleteNoteFromDatabase(noteId, userId) {
        let conn;
        try {
            conn = await pool.getConnection();
            const result = await conn.query(
                'DELETE FROM notes WHERE note_id = ? AND user_id = ?',
                [noteId, userId]
            );
            return result.affectedRows > 0;
        } catch (err) {
            console.error('Database error:', err);
            return false;
        } finally {
            if (conn) conn.release();
        }
    }

    saveNoteToTemporary(username, folderId, title, content, temporaryNotesMap) {
        const userNotes = temporaryNotesMap.get(username) || [];
        
        // Generate unique ID across all notes for this user
        const maxId = userNotes.length > 0 ? Math.max(...userNotes.map(n => n.id)) : 0;
        
        const newNote = {
            id: maxId + 1,
            folderId: parseInt(folderId), // Ensure folderId is integer
            title,
            content,
            createdAt: new Date()
        };
        
        userNotes.push(newNote);
        temporaryNotesMap.set(username, userNotes);
        
        return newNote;
    }

    getNotesFromTemporary(username, folderId = null, temporaryNotesMap) {
        const userNotes = temporaryNotesMap.get(username) || [];
        if (folderId) {
            return userNotes.filter(note => note.folderId === folderId);
        }
        return userNotes;
    }

    deleteNoteFromTemporary(noteId, username, temporaryNotesMap) {
        const userNotes = temporaryNotesMap.get(username) || [];
        const noteIndex = userNotes.findIndex(n => n.id === noteId);
        
        if (noteIndex === -1) return false;
        
        const filteredNotes = userNotes.filter(n => n.id !== noteId);
        temporaryNotesMap.set(username, filteredNotes);
        
        return true;
    }
}

module.exports = { NoteManager };