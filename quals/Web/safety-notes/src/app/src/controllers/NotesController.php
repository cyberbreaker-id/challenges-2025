<?php

class NotesController {
    private $auth;
    private $note;
    private $renderer;
    
    public function __construct($auth, $note, $renderer) {
        $this->auth = $auth;
        $this->note = $note;
        $this->renderer = $renderer;
    }
    
    public function index($req, $res) {
        if (!$this->auth->isLoggedIn()) {
            return ($res->redirect)('/login');
        }
        
        return ($res->html)($this->renderer->render('notes', [
            'notes' => $this->note->findByUserId($this->auth->getCurrentUserId()),
            'username' => $this->auth->getCurrentUser()
        ], $req->cookies ?? []));
    }
    
    public function create($req, $res) {
        if (!$this->auth->isLoggedIn()) {
            return ($res->redirect)('/login');
        }
        
        $this->note->create(
            $this->auth->getCurrentUserId(), 
            $req->postData['title'], 
            $req->postData['content']
        );
        return ($res->redirect)('/notes');
    }
    
    public function delete($req, $res) {
        if (!$this->auth->isLoggedIn()) {
            return ($res->redirect)('/login');
        }
        
        if (isset($req->queryParams['id'])) {
            $this->note->delete($req->queryParams['id'], $this->auth->getCurrentUserId());
        }
        return ($res->redirect)('/notes');
    }
}