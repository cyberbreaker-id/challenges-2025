<?php
ini_set('display_errors', 'Off');error_reporting(0);

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE');

$notesFile = '../notes.json';

function loadNotes() {
    global $notesFile;
    if (file_exists($notesFile)) {
        $json = file_get_contents($notesFile);
        return json_decode($json, true) ?: [];
    }
    return [];
}

function saveNotes($notes) {
    global $notesFile;
    file_put_contents($notesFile, json_encode($notes, JSON_PRETTY_PRINT));
}

function generateId() {
    $pattern = '/[xy]/';
    $template = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx';
    
    return preg_replace_callback($pattern, function($matches) {
        $r = mt_rand(0, 15);
        $v = ($matches[0] === 'x') ? $r : ($r & 0x3 | 0x8);
        return dechex($v);
    }, $template);
}

$method = $_SERVER['REQUEST_METHOD'];
$input = json_decode(file_get_contents('php://input'), true);

switch ($method) {
    case 'GET':
        $notes = loadNotes();
        if (isset($_GET['id'])) {
            $note = array_filter($notes, function($n) {
                return $n['id'] === $_GET['id'];
            });
            echo json_encode(array_values($note)[0] ?? []);
        } else {
            echo json_encode([]);
        }
        break;
        
    case 'POST':
        $notes = loadNotes();
        $newNote = [
            'id' => generateId(),
            'title' => $input['title'] ?? '',
            'content' => $input['content'] ?? '',
            'created' => date('Y-m-d H:i:s')
        ];
        $notes[] = $newNote;
        saveNotes($notes);
        echo json_encode($newNote);
        break;
        
    case 'DELETE':
        $notes = loadNotes();
        $id = $_GET['id'] ?? '';
        $notes = array_filter($notes, function($note) use ($id) {
            return $note['id'] !== $id;
        });
        $notes = array_values($notes);
        saveNotes($notes);
        echo json_encode(['success' => true]);
        break;
        
    default:
        http_response_code(405);
        echo json_encode(['error' => 'Method not allowed']);
        break;
}
?>