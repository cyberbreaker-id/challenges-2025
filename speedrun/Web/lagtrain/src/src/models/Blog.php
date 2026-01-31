<?php

require_once 'Database.php';

class Blog {
    private $db;
    
    public function __construct() {
        $this->db = Database::getInstance()->getConnection();
    }
    
    private function sanitizeInput($input) {
        return $this->db->quote($input);
    }
    
    private function sanitizeId($id) {
        $ban = [
            'char', 'unicode', 'match', 'union', 'join',
            'like', 'glob', '[lr]trim', 'substr', 'load_extension',
            'order', 'blob', "[#\"`-]", '\s'
        ];
        $regexp = '/' . implode('|', $ban) . '/i';
        if (preg_match($regexp, strtolower($id))) {
            return false;
        }
        return (int) $id;
    }
    
    public function getPost($id) {
        return ($this->sanitizeId($id)) ? $this->db->query("SELECT * FROM posts WHERE id = " . $id)->fetch(PDO::FETCH_ASSOC) : '';
    }
    
    public function getAllPosts() {
        $result = $this->db->query("SELECT * FROM posts ORDER BY id");
        return $result->fetchAll(PDO::FETCH_ASSOC);
    }
    
    public function createPost($title, $content, $author, $category = 'General', $tags = '') {
        $id = Database::getInstance()->generateRandomId();
        $title = $this->sanitizeInput($title);
        $content = $this->sanitizeInput($content);
        $author = $this->sanitizeInput($author);
        $category = $this->sanitizeInput($category);
        $tags = $this->sanitizeInput($tags);
        return $this->db->exec("INSERT INTO posts (id, title, content, author, category, tags) VALUES ($id, $title, $content, $author, $category, $tags)");
    }
    
    public function searchPosts($query = '', $searchTag = '', $searchCategory = '') {
        $conditions = [];
        
        if (!empty($query)) {
            $query = $this->sanitizeInput($query);
            $conditions[] = "(title LIKE '%' || $query || '%' OR content LIKE '%' || $query || '%' OR tags LIKE '%' || $query || '%')";
        }
        
        if (!empty($searchTag)) {
            $searchTag = $this->sanitizeInput($searchTag);
            $conditions[] = "tags LIKE '%' || $searchTag || '%'";
        }
        
        if (!empty($searchCategory)) {
            $searchCategory = $this->sanitizeInput($searchCategory);
            $conditions[] = "category = $searchCategory";
        }
        
        if (empty($conditions)) {
            return $this->getAllPosts();
        }
        
        $whereClause = implode(' AND ', $conditions);
        $result = $this->db->query("SELECT * FROM posts WHERE $whereClause ORDER BY id DESC");
        return $result->fetchAll(PDO::FETCH_ASSOC);
    }
    
    public function getPostsByCategory($category) {
        $category = $this->sanitizeInput($category);
        $result = $this->db->query("SELECT * FROM posts WHERE category = $category ORDER BY id DESC");
        return $result->fetchAll(PDO::FETCH_ASSOC);
    }
    
    public function getAllCategories() {
        $result = $this->db->query("SELECT DISTINCT category FROM posts ORDER BY category");
        return $result->fetchAll(PDO::FETCH_COLUMN);
    }
}
?>