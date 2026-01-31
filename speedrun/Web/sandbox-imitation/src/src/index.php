<?php
ini_set('display_errors', 0);ini_set('display_startup_errors', 0);error_reporting(0);
function security_headers(){
    header("Content-Security-Policy: default-src 'none'; connect-src 'none'; sandbox;");
    header("X-Frame-Options: DENY");
    header("X-Content-Type-Options: nosniff");
}
security_headers();
$xss = '';
try {
    $xss = $_REQUEST['xss'] ?? 'free html injection';
    var_dump($xss);
} catch (\Throwable $th) {
}
?>

