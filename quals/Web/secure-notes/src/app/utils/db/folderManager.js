const { pool } = require('./connection');
const { normalizeResult } = require('./helpers');

class FolderManager {
    async createFolder(userId, folderName) {
        let conn;
        try {
            conn = await pool.getConnection();
            const result = await conn.query(
                'INSERT INTO folders (user_id, folder_name) VALUES (?, ?)',
                [userId, folderName]
            );
            return { id: result.insertId, userId, folderName, createdAt: new Date() };
        } catch (err) {
            console.error('Database error:', err);
            throw err;
        } finally {
            if (conn) conn.release();
        }
    }

    async getFoldersByUser(userId) {
        let conn;
        try {
            conn = await pool.getConnection();
            const rows = await conn.query(
                'SELECT folder_id as id, folder_name as name, created_at as createdAt FROM folders WHERE user_id = ? ORDER BY folder_name',
                [userId]
            );
            return normalizeResult(rows);
        } catch (err) {
            console.error('Database error:', err);
            return [];
        } finally {
            if (conn) conn.release();
        }
    }

    async deleteFolder(folderId, userId) {
        let conn;
        try {
            conn = await pool.getConnection();
            const result = await conn.query(
                'DELETE FROM folders WHERE folder_id = ? AND user_id = ?',
                [folderId, userId]
            );
            return result.affectedRows > 0;
        } catch (err) {
            console.error('Database error:', err);
            return false;
        } finally {
            if (conn) conn.release();
        }
    }

    // Temporary folder management methods
    createTemporaryFolder(username, folderName, temporaryFoldersMap) {
        const userFolders = temporaryFoldersMap.get(username) || [];
        
        // Generate unique ID across all folders for this user
        const maxId = userFolders.length > 0 ? Math.max(...userFolders.map(f => f.id)) : 0;
        
        const newFolder = {
            id: maxId + 1,
            name: folderName,
            createdAt: new Date()
        };
        userFolders.push(newFolder);
        temporaryFoldersMap.set(username, userFolders);
        return newFolder;
    }

    getTemporaryFolders(username, temporaryFoldersMap) {
        return temporaryFoldersMap.get(username) || [];
    }

    deleteTemporaryFolder(folderId, username, temporaryFoldersMap, temporaryNotesMap) {
        const userFolders = temporaryFoldersMap.get(username) || [];
        const folderIndex = userFolders.findIndex(f => f.id === folderId);
        
        if (folderIndex === -1) return false;
        
        // Delete all notes in this folder first
        const userNotes = temporaryNotesMap.get(username) || [];
        const filteredNotes = userNotes.filter(n => n.folderId !== folderId);
        temporaryNotesMap.set(username, filteredNotes);
        
        // Delete the folder
        const filteredFolders = userFolders.filter(f => f.id !== folderId);
        temporaryFoldersMap.set(username, filteredFolders);
        
        return true;
    }
}

module.exports = { FolderManager };