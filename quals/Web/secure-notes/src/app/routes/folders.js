const folders = require('express').Router();
const { dbManager } = require('../utils/database');

function requireAuth(req, res, next) {
    if (!req.session.user) {
        return res.redirect('/');
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

folders.use(requireAuth);

async function getUserId(username) {
    return await dbManager.getUserIdFromDatabase(username);
}

folders.get('/api', async (req, res) => {
    try {
        const username = req.session.user.username;
        // const storageType = req.query.storage || 'temporary';
        const storageType = databaseOrTemporary(req.query.storage);
        
        let folders;
        if (storageType === 'database') {
            const userId = await getUserId(username);
            folders = await dbManager.getFoldersByUser(userId);
        } else {
            folders = dbManager.getTemporaryFolders(username);
        }
        
        res.json(folders);
    } catch (error) {
        console.error('Error fetching folders:', error);
        res.status(500).json({ error: 'Failed to fetch folders' });
    }
});

// Create new folder
folders.post('/create', async (req, res) => {
    try {
        const { name, isTemporary } = req.body;
        const username = req.session.user.username;
        
        if (!name) {
            return res.status(400).json({ error: 'Folder name is required' });
        }
        
        let newFolder;
        const isTemporaryFolder = isTemporary === 'true' || isTemporary === true;
        
        if (isTemporaryFolder) {
            newFolder = dbManager.createTemporaryFolder(username, name);
        } else {
            const userId =  await getUserId(username);
            newFolder = await dbManager.createFolder(userId, name);
        }
        
        res.json(newFolder);
    } catch (error) {
        console.error('Error creating folder:', error);
        res.status(500).json({ error: 'Failed to create folder' });
    }
});

// Delete folder
folders.delete('/:id', async (req, res) => {
    try {
        const folderId = parseInt(req.params.id);
        const username = req.session.user.username;
        // const storageType = req.query.storage || 'temporary';
        const storageType = databaseOrTemporary(req.query.storage);
        
        let deleted;
        if (storageType === 'database') {
            const userId = await getUserId(username);
            deleted = await dbManager.deleteFolder(folderId, userId);
        } else {
            deleted = dbManager.deleteTemporaryFolder(folderId, username);
        }
        
        if (!deleted) {
            return res.status(404).json({ error: 'Folder not found' });
        }
        
        res.json({ message: 'Folder deleted successfully' });
    } catch (error) {
        console.error('Error deleting folder:', error);
        res.status(500).json({ error: 'Failed to delete folder' });
    }
});

module.exports = folders;