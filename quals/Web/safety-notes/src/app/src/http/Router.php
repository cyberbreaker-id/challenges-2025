<?php

class Router {
    private $routes;
    
    public function __construct($routes) {
        $this->routes = $routes;
    }
    
    public function handle($req, $res) {
        $method = $req->method;
        $path = $req->path;
        
        if (isset($this->routes[$method][$path])) {
            $handler = $this->routes[$method][$path];
            return call_user_func($handler, $req, $res);
        }
        
        return ($res->html)('<h1>404 Not Found</h1>', 404);
    }
}