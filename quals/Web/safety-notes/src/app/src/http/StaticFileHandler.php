<?php

class StaticFileHandler {
    
    public static function handle($path) {
        $publicDir = __DIR__ . '/../../public';
        $filePath = $publicDir . $path;
        
        $realPath = realpath($filePath);
        $realPublicDir = realpath($publicDir);
        
        if (!$realPath || !$realPublicDir || strpos($realPath, $realPublicDir) !== 0) {
            return new React\Http\Message\Response(
                404,
                ['Content-Type' => 'text/plain'],
                'File not found'
            );
        }
        
        if (!file_exists($filePath) || !is_file($filePath)) {
            return new React\Http\Message\Response(
                404,
                ['Content-Type' => 'text/plain'],
                'File not found'
            );
        }
        
        $mimeTypes = [
            'css' => 'text/css',
            'js' => 'application/javascript',
            'png' => 'image/png',
            'jpg' => 'image/jpeg',
            'jpeg' => 'image/jpeg',
            'gif' => 'image/gif',
            'ico' => 'image/x-icon',
            'svg' => 'image/svg+xml',
            'woff' => 'font/woff',
            'woff2' => 'font/woff2',
            'ttf' => 'font/ttf',
            'eot' => 'application/vnd.ms-fontobject'
        ];
        
        $extension = strtolower(pathinfo($filePath, PATHINFO_EXTENSION));
        $contentType = $mimeTypes[$extension] ?? 'application/octet-stream';
        
        $content = file_get_contents($filePath);
        
        return new React\Http\Message\Response(
            200,
            [
                'Content-Type' => $contentType,
                'Content-Length' => strlen($content)
            ],
            $content
        );
    }
}