<?php

require_once '../models/Database.php';
require_once '../controllers/BlogController.php';

$db = Database::getInstance();
$db->migrate();

$controller = new BlogController();

$id = $_GET['id'] ?? null;

if ($id) {
    $controller->showPost($id);
} else {
    $controller->showAllPosts();
}
?>