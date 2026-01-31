const { pool } = require('./connection');
const { normalizeResult } = require('./helpers');
const { sanitize_tables } = require('../sanitizer');

class SearchManager {
    async searchAcrossFolders(tables, user_id, searchValue, username, temporaryNotesMap, temporaryFoldersMap) {
        try {
            let allResults = [];
            
            // Search database notes
            let conn;
            try {
                tables = tables || 'folders'
                if(typeof tables === 'string') tables = [tables];
                const sanitizedTables = sanitize_tables(tables) || ['folders'];
                
                const tablesList = sanitizedTables.map(table => `\`${table}\``).join(', ');
                let sql = `SELECT * FROM \`notes\`, ${tablesList} WHERE notes.user_id = ? AND notes.folder_id = folders.folder_id AND folders.user_id = ? AND (notes.title LIKE ? OR notes.content LIKE ?)`;
                let params = [user_id, user_id, `%${searchValue}%`, `%${searchValue}%`];
                conn = await pool.getConnection();
                const dbRows = await conn.query(sql, params);
                const normalizedDbResults = normalizeResult(dbRows);
                allResults = allResults.concat(normalizedDbResults);
            } catch (error) {
                console.error('Database search error:', error);
            } finally {
                if (conn) conn.release();
            }

            // Search temporary notes
            if (username) {
                const tempNotes = temporaryNotesMap.get(username) || [];
                const tempFolders = temporaryFoldersMap.get(username) || [];
                
                const matchingTempNotes = tempNotes.filter(note => 
                    note.title.toLowerCase().includes(searchValue.toLowerCase()) ||
                    note.content.toLowerCase().includes(searchValue.toLowerCase())
                );
                
                // Add folder information to temporary notes
                const tempNotesWithFolders = matchingTempNotes.map(note => {
                    const folder = tempFolders.find(f => f.id === note.folderId);
                    return {
                        ...note,
                        folder_name: folder ? folder.name : 'Unknown',
                        user_id: user_id,
                        note_id: note.id
                    };
                });
                
                allResults = allResults.concat(tempNotesWithFolders);
            }
            
            return {
                success: true,
                searchValue: searchValue,
                results: allResults,
            };
        } catch (error) {
            console.error('Search error:', error);
            throw error;
        }
    }
}

module.exports = { SearchManager };