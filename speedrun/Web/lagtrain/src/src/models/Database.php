<?php

class Database {
    private static $instance = null;
    private $pdo;
    
    private function __construct() {
        $this->pdo = new PDO('sqlite:../blog.db');
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
        $postsTable = "CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT DEFAULT 'General',
            tags TEXT DEFAULT '',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )";

        $this->pdo->exec($postsTable);
        
        $result = $this->pdo->query("SELECT COUNT(*) FROM posts");
        $count = $result->fetchColumn();
        
        if ($count == 0) {
            $this->seed();
        }
    }
    
    
    private function seed() {
        $id1 = $this->generateRandomId();
        $id2 = $this->generateRandomId();
        $id3 = $this->generateRandomId();
        
        $this->pdo->exec("INSERT INTO posts (id, title, content, author, category, tags) VALUES 
            ('$id1', 'Why Cats Are Weird', 'My cat keeps staring at the wall for no reason. I think it sees ghosts or maybe it just really likes that particular shade of beige. Either way, cats are mysterious creatures.', 'CatLover42', 'Random', 'cats,weird,pets,mystery'),
            ('$id2', 'The Great Pizza Debate', 'Pineapple on pizza is actually not that bad. Fight me. I also think putting ranch on everything is perfectly acceptable. Food gatekeeping is overrated anyway.', 'FoodieGuru', 'Food', 'pizza,pineapple,food,debate,controversial'),
            ('$id3', 'Random Shower Thoughts', 'If you think about it, cereal is just cold soup. Also, why do we say after dark when it is actually after light? These are the questions that keep me awake at night.', 'ThoughtBubble', 'Philosophy', 'thoughts,random,cereal,soup,existential')");

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