<?php

class CsrfProtection {
    
    public static function generateToken() {
        $token = bin2hex(random_bytes(32));
        return $token;
    }
    
    public static function validateToken($token, $cookies = null) {
        $cookieToken = '';
        if ($cookies && isset($cookies['csrf_token'])) {
            $cookieToken = $cookies['csrf_token'];
        } elseif (isset($_COOKIE['csrf_token'])) {
            $cookieToken = $_COOKIE['csrf_token'];
        }
        
        if (empty($cookieToken) || empty($token)) {
            return false;
        }
        
        if (!self::isValidTokenFormat($cookieToken) || !self::isValidTokenFormat($token)) {
            return false;
        }
        
        return hash_equals($cookieToken, $token);
    }
    
    public static function isValidTokenFormat($token) {
        return is_string($token) && 
               strlen($token) === 64 && 
               ctype_xdigit($token);
    }
    
    public static function getToken($cookies = null) {
        $cookieToken = null;
        if ($cookies && isset($cookies['csrf_token'])) {
            $cookieToken = $cookies['csrf_token'];
        } elseif (isset($_COOKIE['csrf_token'])) {
            $cookieToken = $_COOKIE['csrf_token'];
        }
        
        if (!$cookieToken || !self::isValidTokenFormat($cookieToken)) {
            return self::generateToken();
        }
        return $cookieToken;
    }
    
    public static function regenerateToken() {
        return self::generateToken();
    }
}