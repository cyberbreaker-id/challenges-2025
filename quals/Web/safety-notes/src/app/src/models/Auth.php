<?php

class Auth {
    private $user;
    private $cookies;
    
    public function __construct($cookies = []) {
        $this->user = new User();
        $this->cookies = $cookies;
    }
    
    public function login($username, $password) {
        $user = $this->user->authenticate($username, $password);
        
        if ($user) {
            $sessionId = SessionManager::createSession($user['id'], $user['username']);
            
            return [
                'PHPSESSID' => $sessionId
            ];
        }
        
        return false;
    }
    
    public function register($username, $password) {
        return $this->user->create($username, $password);
    }
    
    public function logout() {
        if (isset($this->cookies['PHPSESSID'])) {
            SessionManager::destroySession($this->cookies['PHPSESSID']);
        }
        return ['PHPSESSID' => ''];
    }
    
    public function isLoggedIn() {
        if (!isset($this->cookies['PHPSESSID'])) {
            return false;
        }
        
        return SessionManager::isValidSession($this->cookies['PHPSESSID']);
    }
    
    public function getCurrentUser() {
        if (!isset($this->cookies['PHPSESSID'])) {
            return null;
        }
        
        $user = SessionManager::getUserFromSession($this->cookies['PHPSESSID']);
        return $user ? $user['username'] : null;
    }
    
    public function getCurrentUserId() {
        if (!isset($this->cookies['PHPSESSID'])) {
            return null;
        }
        
        $user = SessionManager::getUserFromSession($this->cookies['PHPSESSID']);
        return $user ? $user['id'] : null;
    }
    
    public function requireAuth() {
        if (!$this->isLoggedIn()) {
            throw new Exception('Authentication required');
        }
    }
}