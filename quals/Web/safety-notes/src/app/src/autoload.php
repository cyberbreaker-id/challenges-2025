<?php

class Autoloader {
    private static $loadedFiles = [];
    private static $instance = null;
    
    public static function getInstance() {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }
    
    public static function register() {
        spl_autoload_register([self::class, 'loadClass']);
    }
    
    public static function loadClass($className) {
        $baseDir = __DIR__ . '/';
        
        // Map classes to their file paths
        $classMap = [
            'Database' => 'models/Database.php',
            'User' => 'models/User.php',
            'Note' => 'models/Note.php',
            'Auth' => 'models/Auth.php',
            'NotesApp' => 'models/NotesApp.php',
            'TemplateRenderer' => 'views/TemplateRenderer.php',
            'CsrfProtection' => 'security/CsrfProtection.php',
            'SessionManager' => 'security/SessionManager.php',
            'Router' => 'http/Router.php',
            'ResponseHelper' => 'http/ResponseHelper.php',
            'StaticFileHandler' => 'http/StaticFileHandler.php',
            'HomeController' => 'controllers/HomeController.php',
            'AuthController' => 'controllers/AuthController.php',
            'NotesController' => 'controllers/NotesController.php',
        ];
        
        if (isset($classMap[$className])) {
            $filePath = $baseDir . $classMap[$className];
            self::requireOnce($filePath);
        }
    }
    
    public static function requireOnce($filePath) {
        $realPath = realpath($filePath);
        
        if ($realPath && !in_array($realPath, self::$loadedFiles)) {
            require_once $filePath;
            self::$loadedFiles[] = $realPath;
        }
    }
    
    public static function loadConfig() {
        static $config = null;
        if ($config === null) {
            $config = require __DIR__ . '/../config.php';
        }
        return $config;
    }
    
    public static function getRoutes($renderer, $cookies = []) {
        // Create new instances for each request to avoid shared state
        $auth = new Auth($cookies);
        $note = new Note();
        
        $homeController = new HomeController($auth);
        $authController = new AuthController($auth, $renderer);
        $notesController = new NotesController($auth, $note, $renderer);
        
        $routes = [
            'GET' => [
                '/' => [$homeController, 'index'],
                '/login' => [$authController, 'loginGet'],
                '/register' => [$authController, 'registerGet'],
                '/logout' => [$authController, 'logout'],
                '/notes' => [$notesController, 'index'],
                '/delete-note' => [$notesController, 'delete'],
            ],
            'POST' => [
                '/login' => [$authController, 'loginPost'],
                '/register' => [$authController, 'registerPost'],
                '/notes' => [$notesController, 'create'],
            ]
        ];
        return $routes;
    }
}