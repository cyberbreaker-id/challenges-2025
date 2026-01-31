const { pool } = require('./connection');
const crypto = require('crypto')
class MigrationManager {
    async migrate() {
        let conn;

        try {
            console.log("[+] Migratin Started")
            console.log(`${process.env.ADMIN_USERNAME} : ${process.env.ADMIN_PASSWORD}`)
            conn = await pool.getConnection();
            
            const stmts = [
                `DROP TABLE IF EXISTS notes;`,
                `DROP TABLE IF EXISTS folders;`,
                `DROP TABLE IF EXISTS users;`,

                `CREATE TABLE users (
                    user_id INTEGER AUTO_INCREMENT PRIMARY KEY,
                    username TEXT,
                    password TEXT
                );`,

                `CREATE TABLE folders (
                    folder_id INTEGER AUTO_INCREMENT PRIMARY KEY,
                    user_id INTEGER,
                    folder_name TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                );`,

                `CREATE TABLE notes (
                    note_id INTEGER AUTO_INCREMENT PRIMARY KEY,
                    user_id INTEGER,
                    folder_id INTEGER,
                    title TEXT,
                    content TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    FOREIGN KEY (folder_id) REFERENCES folders(folder_id) ON DELETE CASCADE
                );`,

                // Insert demo users with MD5 hashed passwords
                `INSERT INTO users (username, password) VALUES ('${process.env.ADMIN_USERNAME}', '${crypto.createHash('md5').update(process.env.ADMIN_PASSWORD).digest('hex')}');`,
                // `INSERT INTO users (username, password) VALUES ('user', '5f4dcc3b5aa765d61d8327deb882cf99');`,   // password in MD5
                
                `INSERT INTO folders (user_id, folder_name) VALUES (1, 'General');`,
                // `INSERT INTO folders (user_id, folder_name) VALUES (2, 'General');`,
            ];
            
            for (const stmt of stmts) {
                console.log(`[+] Executing: ${stmt.substring(0, 50)}...`);
                await conn.query(stmt);
            }
            
            console.log("[+] Migration completed successfully");
        } catch (err) {
            console.error("[!] Migration error:", err);
        } finally {
            if (conn) conn.release();
        }
    }
}

module.exports = { MigrationManager };