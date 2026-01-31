<?php
error_reporting(0);

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['note'])) {
    $note = $_POST['note'];

    $filename = 'uploads/' . bin2hex(random_bytes(8)) . '.txt';
    file_put_contents($filename, $note);

    echo "Note saved! File: $filename";
    exit;
}

if (isset($_GET['url'])) {
    if (!isset($_GET['debug']) || $_GET['debug'] != 1) {
        die("under maintenance");
    }

    $url = $_GET['url'];

    $output = [];
    $status = 0;

    exec("curl -Is " . escapeshellarg($url) . " | head -n 1", $output, $status);

    echo "<pre>" . htmlspecialchars(implode("\n", $output)) . "</pre>";
    exit;
}

?>

<h2>Save a Note</h2>
<form method="POST">
    <textarea name="note" placeholder="Enter your note"></textarea><br>
    <button type="submit">Save Note</button>
</form>
