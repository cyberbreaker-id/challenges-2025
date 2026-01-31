<?php

class Note {
    private $db;
    
    public function __construct() {
        $this->db = Database::getInstance();
    }
    
    public function create($userId, $title, $content) {
        if (empty($userId) || empty($title) || empty($content)) {
            return false;
        }
        
        $result = $this->db->execute(
            'INSERT INTO notes (user_id, title, content) VALUES (?, ?, ?)',
            [
                $userId,
                htmlspecialchars($title, ENT_QUOTES, 'UTF-8'),
                htmlspecialchars($content, ENT_QUOTES, 'UTF-8')
            ]
        );
        
        return $result > 0;
    }
    
    public function findById($id) {
        return $this->db->fetch(
            'SELECT id, user_id, title, content, created_at, updated_at 
             FROM notes 
             WHERE id = ?',
            [$id]
        );
    }
    
    public function findByUserId($userId) {
        return $this->db->fetchAll(
            'SELECT id, title, content, created_at, updated_at 
             FROM notes 
             WHERE user_id = ? 
             ORDER BY created_at DESC',
            [$userId]
        );
    }
    
    public function update($id, $userId, $title, $content) {
        if (empty($title) || empty($content)) {
            return false;
        }
        
        $result = $this->db->execute(
            'UPDATE notes 
             SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP 
             WHERE id = ? AND user_id = ?',
            [
                htmlspecialchars($title, ENT_QUOTES, 'UTF-8'),
                htmlspecialchars($content, ENT_QUOTES, 'UTF-8'),
                $id,
                $userId
            ]
        );
        
        return $result > 0;
    }
    
    public function delete($id, $userId) {
        $result = $this->db->execute(
            'DELETE FROM notes WHERE id = ? AND user_id = ?',
            [$id, $userId]
        );
        
        return $result > 0;
    }
    
    public function belongsToUser($id, $userId) {
        $note = $this->db->fetch(
            'SELECT user_id FROM notes WHERE id = ?',
            [$id]
        );
        
        return $note && $note['user_id'] == $userId;
    }
}