<?php

class ResponseHelper {
    private $config;
    
    public function __construct($config) {
        $this->config = $config;
    }
    
    public function createResponseObject() {
        $res = new stdClass();
        
        $res->json = function($data, $status = 200) {
            return new React\Http\Message\Response(
                $status,
                ['Content-Type' => 'application/json'],
                json_encode($data)
            );
        };
        
        $res->html = function($content, $status = 200) use ($res) {
            $headers = ['Content-Type' => 'text/html'];
            if (!isset($res->cookies['csrf_token'])) {
                $token = CsrfProtection::generateToken();
                $headers['Set-Cookie'] = sprintf(
                    'csrf_token=%s; Path=/; HttpOnly; SameSite=Strict; Max-Age=3600',
                    $token
                );
            }
            
            return new React\Http\Message\Response($status, $headers, $content);
        };
        
        $res->text = function($content, $status = 200) {
            return new React\Http\Message\Response(
                $status,
                ['Content-Type' => 'text/plain'],
                $content
            );
        };
        
        $res->redirect = function($location, $cookies = []) use ($res) {
            $baseUri = $this->config['base_uri'] ?? '';
            $fullLocation = $baseUri . $location;
            
            $headers = ['Location' => $fullLocation];
            $cookieHeaders = [];
            
            foreach ($cookies as $name => $value) {
                if (empty($value)) {
                    $cookieHeaders[] = sprintf(
                        '%s=%s; Path=/; HttpOnly; SameSite=Strict; Max-Age=0; Expires=Thu, 01 Jan 1970 00:00:00 GMT',
                        $name,
                        $value
                    );
                } else {
                    $cookieHeaders[] = sprintf(
                        '%s=%s; Path=/; HttpOnly; SameSite=Strict; Max-Age=86400',
                        $name,
                        $value
                    );
                }
            }
            
            if ($cookieHeaders) {
                $headers['Set-Cookie'] = $cookieHeaders;
            }
            
            return new React\Http\Message\Response(302, $headers, '');
        };
        
        return $res;
    }
}