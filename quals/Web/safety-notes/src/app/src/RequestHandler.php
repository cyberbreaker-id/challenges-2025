<?php

class RequestHandler {
    private $app;
    private $renderer;
    private $config;
    
    public function __construct($app, $renderer, $config) {
        $this->app = $app;
        $this->renderer = $renderer;
        $this->config = $config;
    }
    
    public function handle($req, $res) {
        switch ($req->path) {
            case '/':
                if ($this->app->isLoggedIn()) {
                    return ($res->redirect)('/notes');
                }
                return ($res->redirect)('/login');

            case '/login':
                if ($req->method === 'POST') {
                    if ($this->app->login($req->postData['username'], $req->postData['password'])) {
                        return ($res->redirect)('/notes');
                    }
                    return ($res->html)($this->renderer->render('login', ['error' => 'Invalid credentials']));
                }
                
                if ($this->app->isLoggedIn()) {
                    return ($res->redirect)('/notes');
                }
                return ($res->html)($this->renderer->render('login'));

            case '/register':
                if ($req->method === 'POST') {
                    if ($this->app->register($req->postData['username'], $req->postData['password'])) {
                        return ($res->redirect)('/login');
                    }
                    return ($res->html)($this->renderer->render('register', ['error' => 'Username already exists']));
                }
                return ($res->html)($this->renderer->render('register'));

            case '/logout':
                $this->app->logout();
                return ($res->redirect)('/login');

            case '/notes':
                if (!$this->app->isLoggedIn()) {
                    return ($res->redirect)('/login');
                }
                
                if ($req->method === 'POST') {
                    $this->app->addNote($req->postData['title'], $req->postData['content']);
                    return ($res->redirect)('/notes');
                }
                
                return ($res->html)($this->renderer->render('notes', [
                    'notes' => $this->app->getUserNotes(),
                    'username' => $this->app->getCurrentUser()
                ]));

            case '/delete-note':
                if (!$this->app->isLoggedIn()) {
                    return ($res->redirect)('/login');
                }
                
                if (isset($req->queryParams['id'])) {
                    $this->app->deleteNote($req->queryParams['id']);
                }
                return ($res->redirect)('/notes');

            default:
                return ($res->html)('<h1>404 Not Found</h1>', 404);
        }
    }
}