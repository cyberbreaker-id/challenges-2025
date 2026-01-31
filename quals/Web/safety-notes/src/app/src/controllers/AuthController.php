<?php

class AuthController {
    private $auth;
    private $renderer;
    
    public function __construct($auth, $renderer) {
        $this->auth = $auth;
        $this->renderer = $renderer;
    }
    
    public function loginGet($req, $res) {
        if ($this->auth->isLoggedIn()) {
            return ($res->redirect)('/notes');
        }
        return ($res->html)($this->renderer->render('login', [], $req->cookies ?? []));
    }
    
    public function loginPost($req, $res) {
        $authCookies = $this->auth->login($req->postData['username'], $req->postData['password']);
        if ($authCookies) {
            return ($res->redirect)('/notes', $authCookies);
        }
        return ($res->html)($this->renderer->render('login', ['error' => 'Invalid credentials'], $req->cookies ?? []));
    }
    
    public function registerGet($req, $res) {
        return ($res->html)($this->renderer->render('register', [], $req->cookies ?? []));
    }
    
    public function registerPost($req, $res) {
        if ($this->auth->register($req->postData['username'], $req->postData['password'])) {
            return ($res->redirect)('/login');
        }
        return ($res->html)($this->renderer->render('register', ['error' => 'Username already exists'], $req->cookies ?? []));
    }
    
    public function logout($req, $res) {
        $expiredCookies = $this->auth->logout();
        return ($res->redirect)('/login', $expiredCookies);
    }
}