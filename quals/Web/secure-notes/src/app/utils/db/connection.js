const mariadb = require('mariadb');

const pool = mariadb.createPool({
    // host: process.env.DB_HOST || 'localhost',
    // port: process.env.DB_PORT || '3306',
    socketPath: "/var/run/mysqld/mysqld.sock",
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || 'example',
    database: process.env.DB_NAME || 'secure_notes',
    nestTables: true,
    connectionLimit: 5,
});

module.exports = { pool };