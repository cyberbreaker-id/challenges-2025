<?php

use Twig\Environment;
use Twig\Loader\FilesystemLoader;

class TemplateRenderer {
    private $twig;
    private $config;
    
    public function __construct($templatePath = 'templates/', $host = null) {
        $this->config = Autoloader::loadConfig();
        
        $loader = new FilesystemLoader($templatePath);
        $this->twig = new Environment($loader, [
            'cache' => $this->config['cache_templates'],
            'debug' => $this->config['debug'],
            'auto_reload' => true
        ]);
        
        $baseUrl = $this->config['get_base_url']($host);
        
        $this->twig->addGlobal('config', $this->config);
        $this->twig->addGlobal('base_uri', $this->config['base_uri']);
        $this->twig->addGlobal('base_url', $baseUrl);
    }
    
    public function render($template, $data = [], $cookies = []) {
        try {
            if (!isset($data['csrf_token'])) {
                if (isset($cookies['csrf_token']) && CsrfProtection::isValidTokenFormat($cookies['csrf_token'])) {
                    $data['csrf_token'] = $cookies['csrf_token'];
                } else {
                    $token = CsrfProtection::generateToken();
                    $data['csrf_token'] = $token;
                }
            }
            
            return $this->twig->render($template . '.twig', $data);
        } catch (Exception $e) {
            throw new Exception("Template rendering error: " . $e->getMessage());
        }
    }
}