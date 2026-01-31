<?php
    error_reporting(0);

    $key = "CBC{19f8b477079d7e43d171b54fd32e69f3}";

    if (isset($_POST['key'])) {
        if (strcmp($_POST['key'], $key) == 0) {
            echo htmlspecialchars($key);
        } else {
            echo "Die";
        }
    }
?>

<html>
<head>
    <title> Secret Vault </title>
</head>
<body>
    <h2>Enter the secret key</h2>
    <form action="index.php" method="POST">
        <label for="key">Key:</label>
        <input type="password" id="key" name="key">
        <button type="submit">Unlock</button>
    </form>
</body>
</html>
