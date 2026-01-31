<?php

if (!function_exists('getBaseUrl')) {
    function getBaseUrl($host = null) {
        if (!preg_match('/^[a-zA-Z0-9.\-:,\s\?]+$/', $host)) {
            $host = 'localhost';
        }
        
        $protocol = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on') ? 'https://' : 'http://';
        return $protocol . $host;
    }
}

return [
    'base_uri' => $_ENV['BASE_URI'] ?? '',
    'app_name' => 'Safety Notes',
    'debug' => false,
    'cache_templates' => false,
    'get_base_url' => 'getBaseUrl',
];