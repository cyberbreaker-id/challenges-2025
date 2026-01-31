<?php

require_once 'Database.php';

class User {
    private $db;
    
    public function __construct() {
        $this->db = Database::getInstance()->getConnection();
    }

    function quote($input) {
        return (str_contains($input, "'")) ? false : $input;
    }
    
    private function sanitizeInput($input) {
        return $this->quote($input);
    }
    
    public function authenticateUser($username, $password) {
        $username = $this->sanitizeInput($username);
        $password = $this->sanitizeInput($password);
        if(!$username && !$password){
            return [];
        }
        $result = $this->db->query("SELECT * FROM users WHERE username = '$username' AND password = '$password'");
        return $result->fetch(PDO::FETCH_ASSOC);
    }
}
?>