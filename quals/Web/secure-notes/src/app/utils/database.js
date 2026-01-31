// Import all modular managers
const { pool } = require('./db/connection');
const { MigrationManager } = require('./db/migration');
const { UserManager } = require('./db/userManager');
const { FolderManager } = require('./db/folderManager');
const { NoteManager } = require('./db/noteManager');
const { SearchManager } = require('./db/searchManager');

class DatabaseManager {
    constructor() {
        this.temporaryNotesMap = new Map();
        this.temporaryFoldersMap = new Map();
        
        // Initialize managers
        this.migrationManager = new MigrationManager();
        this.userManager = new UserManager();
        this.folderManager = new FolderManager();
        this.noteManager = new NoteManager();
        this.searchManager = new SearchManager();
        
        
    }

    async migrate() {
        // Initialize admin temporary folders and notes
        this.temporaryFoldersMap.set('admin', [
            { id: 1, name: 'General', createdAt: new Date() }
        ]);
        
        this.temporaryNotesMap.set('admin', [
            { id: 1, folderId: 1, title: "Secure Flag", content: `This is truly a secure notes!, this is the flag ${process.env.FLAG || 'CBC{fake_flag}'}`, createdAt: new Date() }
        ]);

        return await this.migrationManager.migrate();
        
    }

    // Database folder methods
    async createFolder(userId, folderName) {
        return await this.folderManager.createFolder(userId, folderName);
    }

    async getFoldersByUser(userId) {
        return await this.folderManager.getFoldersByUser(userId);
    }

    async deleteFolder(folderId, userId) {
        return await this.folderManager.deleteFolder(folderId, userId);
    }

    // Database note methods
    async saveNoteToDatabase(userId, folderId, title, content) {
        return await this.noteManager.saveNoteToDatabase(userId, folderId, title, content);
    }

    async getNotesFromDatabase(userId, folderId = null) {
        return await this.noteManager.getNotesFromDatabase(userId, folderId);
    }

    async deleteNoteFromDatabase(noteId, userId) {
        return await this.noteManager.deleteNoteFromDatabase(noteId, userId);
    }

    // Temporary folder management methods
    createTemporaryFolder(username, folderName) {
        return this.folderManager.createTemporaryFolder(username, folderName, this.temporaryFoldersMap);
    }

    getTemporaryFolders(username) {
        return this.folderManager.getTemporaryFolders(username, this.temporaryFoldersMap);
    }

    deleteTemporaryFolder(folderId, username) {
        return this.folderManager.deleteTemporaryFolder(folderId, username, this.temporaryFoldersMap, this.temporaryNotesMap);
    }

    // Temporary note methods
    saveNoteToTemporary(username, folderId, title, content) {
        return this.noteManager.saveNoteToTemporary(username, folderId, title, content, this.temporaryNotesMap);
    }

    getNotesFromTemporary(username, folderId = null) {
        return this.noteManager.getNotesFromTemporary(username, folderId, this.temporaryNotesMap);
    }

    deleteNoteFromTemporary(noteId, username) {
        return this.noteManager.deleteNoteFromTemporary(noteId, username, this.temporaryNotesMap);
    }

    // User management methods
    async registerUser(username, hashedPassword) {
        const result = await this.userManager.registerUser(username, hashedPassword);
        
        // Create default temporary folder for new user
        if (result.success) {
            this.createTemporaryFolder(username, 'General');
        }
        
        return result;
    }

    async verifyUser(username, hashedPassword) {
        return await this.userManager.verifyUser(username, hashedPassword);
    }

    async getUserIdFromDatabase(username) {
        return await this.userManager.getUserIdFromDatabase(username);
    }

    // Search methods
    async searchAcrossFolders(tables, user_id, searchValue, username) {
        return await this.searchManager.searchAcrossFolders(tables, user_id, searchValue, username, this.temporaryNotesMap, this.temporaryFoldersMap);
    }
}

const dbManager = new DatabaseManager();

module.exports = {
    dbManager,
    pool
};
