const user = require('express').Router();
const path = require('path');
const crypto = require('crypto');
const { dbManager } = require('../utils/database');

user.post('/login', async (req, res) => {
    try {
        const { username, password } = req.body;
        
        if (!username || !password) {
            return res.redirect('/?error=missing_fields');
        }
        
        // Hash password with MD5
        const hashedPassword = crypto.createHash('md5').update(password).digest('hex');
        
        // Check against database
        const dbUser = await dbManager.verifyUser(username, hashedPassword);
        
        if (dbUser) {
            req.session.user = { username: dbUser.username, userId: dbUser.user_id };
            res.redirect('/note');
        } else {
            res.redirect('/?error=invalid');
        }
        
    } catch (error) {
        console.error('Login error:', error);
        res.redirect('/?error=server_error');
    }
});

user.get('/logout', (req, res) => {
    req.session.destroy((err) => {
        if (err) {
            return res.status(500).send('Could not log out');
        }
        res.redirect('/');
    });
});

// Show registration form
user.get('/register', (req, res) => {
    res.sendFile(path.join(__dirname, '../templates/register.html'));
});

// Handle registration
user.post('/register', async (req, res) => {
    try {
        const { username, password, confirmPassword } = req.body;
        
        // Basic validation
        if (!username || !password || !confirmPassword) {
            return res.redirect('/user/register?error=missing_fields');
        }
        
        if (password !== confirmPassword) {
            return res.redirect('/user/register?error=password_mismatch');
        }
        
        if (username.length < 3) {
            return res.redirect('/user/register?error=username_too_short');
        }
        
        if (!/^[a-z0-9_.]+$/.test(username)) {
            return res.redirect('/user/register?error=invalid_username');
        }
        
        if (password.length < 6) {
            return res.redirect('/user/register?error=password_too_short');
        }
        
        // Hash password with MD5
        const hashedPassword = crypto.createHash('md5').update(password).digest('hex');
        
        // Try to register user
        const result = await dbManager.registerUser(username, hashedPassword);
        
        if (result.success) {
            // Auto-login after successful registration
            req.session.user = { username: username, userId: result.userId };
            res.redirect('/note');
        } else {
            res.redirect('/user/register?error=' + result.error);
        }
        
    } catch (error) {
        console.error('Registration error:', error);
        res.redirect('/user/register?error=server_error');
    }
});

module.exports = user;