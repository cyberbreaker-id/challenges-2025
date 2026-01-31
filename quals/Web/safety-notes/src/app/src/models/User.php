<?php

class User {
    private $db;
    
    public function __construct() {
        $this->db = Database::getInstance();
    }
    
    public function create($username, $password) {
        if (empty($username) || empty($password)) {
            return false;
        }
        
        // Check if user already exists
        $existingUser = $this->db->fetch(
            'SELECT id FROM users WHERE username = ?', 
            [$username]
        );
        
        if ($existingUser) {
            return false;
        }
        
        // Create new user
        $passwordHash = password_hash($password, PASSWORD_DEFAULT);
        $result = $this->db->execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            [$username, $passwordHash]
        );
        
        return $result > 0;
    }
    
    public function authenticate($username, $password) {
        if (empty($username) || empty($password)) {
            return false;
        }
        
        $user = $this->db->fetch(
            'SELECT id, username, password_hash FROM users WHERE username = ?',
            [$username]
        );
        
        if (!$user) {
            return false;
        }
        
        if (password_verify($password, $user['password_hash'])) {
            return $user;
        }
        
        return false;
    }
    
    public function findById($id) {
        return $this->db->fetch(
            'SELECT id, username, created_at FROM users WHERE id = ?',
            [$id]
        );
    }
    
    public function findByUsername($username) {
        return $this->db->fetch(
            'SELECT id, username, created_at FROM users WHERE username = ?',
            [$username]
        );
    }
}