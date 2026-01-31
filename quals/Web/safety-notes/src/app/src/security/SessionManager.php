<?php

class SessionManager {
    private static $sessions = [];
    private static $sessionLifetime = 3600 * 24;
    
    public static function generateSessionId() {
        return bin2hex(random_bytes(32));
    }
    
    public static function createSession($userId, $username) {
        $sessionId = self::generateSessionId();
        self::$sessions[$sessionId] = [
            'user_id' => $userId,
            'username' => $username,
            'created_at' => time(),
            'last_access' => time()
        ];
        
        self::cleanExpiredSessions();
        
        return $sessionId;
    }
    
    public static function getSession($sessionId) {
        if (!isset(self::$sessions[$sessionId])) {
            return null;
        }
        
        $session = self::$sessions[$sessionId];
        
        if (time() - $session['last_access'] > self::$sessionLifetime) {
            unset(self::$sessions[$sessionId]);
            return null;
        }
        
        self::$sessions[$sessionId]['last_access'] = time();
        
        return $session;
    }
    
    public static function destroySession($sessionId) {
        unset(self::$sessions[$sessionId]);
    }
    
    public static function isValidSession($sessionId) {
        return self::getSession($sessionId) !== null;
    }
    
    private static function cleanExpiredSessions() {
        $now = time();
        foreach (self::$sessions as $sessionId => $session) {
            if ($now - $session['last_access'] > self::$sessionLifetime) {
                unset(self::$sessions[$sessionId]);
            }
        }
    }
    
    public static function getUserFromSession($sessionId) {
        $session = self::getSession($sessionId);
        return $session ? [
            'id' => $session['user_id'],
            'username' => $session['username']
        ] : null;
    }
}