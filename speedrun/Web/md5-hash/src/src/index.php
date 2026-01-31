<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $file = $_POST['file'] ?? null;
    if ($file) {
        echo "MD5: " . md5_file($file);
    } else {
        echo "File not found or not provided.";
    }
} else {
?>
<!DOCTYPE html>
<html>
<head>
    <title>MD5 File (by Path)</title>
</head>
<body>
    <h2>Enter a file path</h2>
    <form method="post">
        <input type="text" name="file" placeholder="/path/to/file" required>
        <button type="submit">Get MD5</button>
    </form>
</body>
</html>
<?php
}
?>
