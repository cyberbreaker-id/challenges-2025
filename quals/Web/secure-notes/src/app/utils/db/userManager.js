const { pool } = require('./connection');
const { normalizeResult } = require('./helpers');

class UserManager {
    async registerUser(username, hashedPassword) {
        let conn;
        try {
            conn = await pool.getConnection();
            
            // Check if username already exists
            let existingUser = await conn.query(
                'SELECT username FROM users WHERE username = ?',
                [username]
            );
            existingUser = normalizeResult(existingUser);
            
            if (existingUser.length > 0) {
                return { success: false, error: 'username_exists' };
            }
            
            // Insert new user
            const result = await conn.query(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                [username, hashedPassword]
            );
            
            const userId = result.insertId;
            
            // Create default General folder for new user
            await conn.query(
                'INSERT INTO folders (user_id, folder_name) VALUES (?, ?)',
                [userId, 'General']
            );
            
            return { success: true, userId: userId };
            
        } catch (err) {
            console.error('Registration error:', err);
            return { success: false, error: 'server_error' };
        } finally {
            if (conn) conn.release();
        }
    }

    async verifyUser(username, hashedPassword) {
        let conn;
        try {
            conn = await pool.getConnection();
            
            let users = await conn.query(
                'SELECT user_id, username FROM users WHERE username = ? AND password = ?',
                [username, hashedPassword]
            );
            users = normalizeResult(users);
            
            return users.length > 0 ? users[0] : null;
            
        } catch (err) {
            console.error('Login verification error:', err);
            return null;
        } finally {
            if (conn) conn.release();
        }
    }

    async getUserIdFromDatabase(username) {
        let conn;
        try {
            conn = await pool.getConnection();
            
            let users = await conn.query(
                'SELECT user_id FROM users WHERE username = ?',
                [username]
            );
            users = normalizeResult(users);

            if (users.length > 0) {
                return users[0].user_id;
            }
            
            return null; // User not found
            
        } catch (err) {
            console.error('Get user ID error:', err);
            return null;
        } finally {
            if (conn) conn.release();
        }
    }
}

module.exports = { UserManager };