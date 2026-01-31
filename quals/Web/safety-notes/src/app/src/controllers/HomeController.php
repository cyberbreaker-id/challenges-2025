<?php

class HomeController {
    private $auth;
    
    public function __construct($auth) {
        $this->auth = $auth;
    }
    
    public function index($req, $res) {
        if ($this->auth->isLoggedIn()) {
            return ($res->redirect)('/notes');
        }
        return ($res->redirect)('/login');
    }
}