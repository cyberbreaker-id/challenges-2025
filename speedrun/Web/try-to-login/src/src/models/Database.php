<?php

class Database {
    private static $instance = null;
    private $pdo;
    
    private function __construct() {
        $host = 'mysqllogin';
        $dbname = 'login_db';
        $username = 'root';
        $password = '';
        
        $this->pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
        $this->pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    }
    
    public static function getInstance() {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }
    
    public function getConnection() {
        return $this->pdo;
    }

    public function generateRandomId() {
        return mt_rand(10000000, 999999999);
    }

    function generateRandomString($length = 10) {
        return substr(str_shuffle(str_repeat($x='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', ceil($length/strlen($x)) )),1,$length);
    }
    
    public function migrate() {
        $usersTable = "CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(20) PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255) DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )";

        $this->pdo->exec($usersTable);
        
        $result = $this->pdo->query("SELECT COUNT(*) FROM users");
        $count = $result->fetchColumn();
        
        if ($count == 0) {
            $this->seed();
        }
    }
    
    
    private function seed() {
        $id1 = $this->generateRandomId();
        $password = $this->generateRandomString();
        
        $this->pdo->exec("INSERT INTO users (id, username, password, email) VALUES 
            ('$id1', 'admin', '$password', 'admin@example.com')");

        $flag = file_get_contents('/flag.txt');
        $tableFlag = 'flag';
        $columnFlag = 'nice';
        $this->pdo->exec("CREATE TABLE IF NOT EXISTS " . $tableFlag . " (
            " . $columnFlag . " TEXT
        )");
        $this->pdo->exec("INSERT INTO $tableFlag ($columnFlag) VALUES ('$flag')");
    }
}
?>