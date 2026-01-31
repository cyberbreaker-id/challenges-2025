<?php

require __DIR__ . '/vendor/autoload.php';
require __DIR__ . '/src/autoload.php';

Autoloader::register();

$config = Autoloader::loadConfig();

$http = new React\Http\HttpServer(
    new React\Http\Middleware\StreamingRequestMiddleware(),
    function (Psr\Http\Message\ServerRequestInterface $request) use ($config) {
        $req = new stdClass();
        $req->path = $request->getUri()->getPath();
        $req->method = $request->getMethod();
        $req->query = $request->getUri()->getQuery();
        $req->host = $request->getHeaderLine('X-Forwarded-Host') ?: $request->getHeaderLine('Host');
        $req->body = $request->getBody();
        $req->headers = $request->getHeaders();
        parse_str($req->query, $req->queryParams);
        
        $req->cookies = [];
        $cookieHeader = $request->getHeaderLine('Cookie');
        if ($cookieHeader) {
            $cookies = explode(';', $cookieHeader);
            foreach ($cookies as $cookie) {
                $parts = explode('=', trim($cookie), 2);
                if (count($parts) === 2) {
                    $req->cookies[trim($parts[0])] = trim($parts[1]);
                }
            }
        }
        
        $responseHelper = new ResponseHelper($config);
        $res = $responseHelper->createResponseObject();
        
        $res->cookies = $req->cookies;
        
        $renderer = new TemplateRenderer('templates/', $req->host);
        $router = new Router(Autoloader::getRoutes($renderer, $req->cookies));

        if (preg_match('/\.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$/i', $req->path)) {
            return StaticFileHandler::handle($req->path);
        }

        if ($req->method === 'POST') {
            return new React\Promise\Promise(function ($resolve, $reject) use ($req, $res, $router, $request) {
                $postBody = '';
                $req->body->on('data', function ($data) use (&$postBody) {
                    $postBody .= $data;
                });

                $req->body->on('end', function () use ($resolve, &$postBody, $req, $res, $router, $request) {
                    $contentType = $request->getHeaderLine('Content-Type');
                    $req->postData = [];
                    
                    if ($contentType && str_contains($contentType, 'application/x-www-form-urlencoded')) {
                        parse_str($postBody, $req->postData);
                        
                        if (!isset($req->postData['csrf_token']) || !CsrfProtection::validateToken($req->postData['csrf_token'], $req->cookies)) {
                            $resolve(($res->text)('CSRF token validation failed', 403));
                            return;
                        }
                    } else {
                        $req->rawBody = $postBody;
                    }
                    
                    $resolve($router->handle($req, $res));
                });
            });
        }

        return $router->handle($req, $res);
    }
);

$http->on('error', function (Exception $e) {
    error_log('Error: ' . $e->getMessage());
});

$socket = new React\Socket\SocketServer($argv[1] ?? '0.0.0.0:8080');
$http->listen($socket);

error_log('Listening on ' . str_replace('tcp:', 'http:', $socket->getAddress()));