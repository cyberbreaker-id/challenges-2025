<?php

require_once '../models/User.php';

class AuthController {
    private $userModel;
    
    public function __construct() {
        $this->userModel = new User();
    }
    
    public function showLogin() {
        $error = $_GET['error'] ?? '';
        $this->renderView('login', ['error' => $error]);
    }
    
    public function processLogin() {
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $username = $_POST['username'] ?? '';
            $password = $_POST['password'] ?? '';
            
            if (empty($username) || empty($password)) {
                header('Location: index.php?error=Please fill in all fields');
                exit;
            }
            
            $user = $this->userModel->authenticateUser($username, $password);
            
            if ($user) {
                session_start();
                $_SESSION['user_id'] = $user['id'];
                $_SESSION['username'] = $user['username'];
                header('Location: index.php?action=dashboard');
                exit;
            } else {
                header('Location: index.php?error=Invalid username or password');
                exit;
            }
        }
    }
    
    public function showDashboard() {
        session_start();
        if (!isset($_SESSION['user_id'])) {
            header('Location: index.php');
            exit;
        }
        
        $user = $_SESSION;
        $this->renderView('dashboard', ['user' => $user]);
    }
    
    public function logout() {
        session_start();
        session_destroy();
        header('Location: index.php');
        exit;
    }
    
    private function renderView($viewName, $data = []) {
        extract($data);
        include "../views/{$viewName}.php";
    }
}
?>