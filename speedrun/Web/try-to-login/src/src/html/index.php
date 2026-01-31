<?php

require_once '../models/Database.php';
require_once '../controllers/AuthController.php';

$db = Database::getInstance();
$db->migrate();

$controller = new AuthController();

$action = $_GET['action'] ?? null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $controller->processLogin();
} elseif ($action === 'dashboard') {
    $controller->showDashboard();
} elseif ($action === 'logout') {
    $controller->logout();
} else {
    $controller->showLogin();
}
?>