<?php

require_once __DIR__ . '/src/controllers/HomeController.php';
require_once __DIR__ . '/src/controllers/AuthController.php';
require_once __DIR__ . '/src/controllers/NotesController.php';
require_once __DIR__ . '/src/models/Auth.php';
require_once __DIR__ . '/src/models/Note.php';

function getRoutes($renderer) {
    $auth = new Auth();
    $note = new Note();
    
    $homeController = new HomeController($auth);
    $authController = new AuthController($auth, $renderer);
    $notesController = new NotesController($auth, $note, $renderer);
    
    return [
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
}