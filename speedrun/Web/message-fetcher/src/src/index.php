<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['url'])) {
    $data = @file_get_contents($_POST['url']);
    $data = @json_decode($data);
    echo "<h3>Server Response:</h3>";
    if ($data && isset($data->msg)) {
        echo htmlspecialchars($data->msg);
    } else {
        echo "Invalid response.";
    }
} else {
    echo "Die.";
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Message Fetcher</title>
</head>
<body>
    <h2>Message Fetcher</h2>
    <form method="POST">
        <label for="url">Enter a URL:</label><br>
        <input type="text" id="url" name="url" placeholder="http://example.com/data.json" style="width:400px;"><br><br>
        <input type="submit" value="Fetch">
    </form>
</body>
</html>