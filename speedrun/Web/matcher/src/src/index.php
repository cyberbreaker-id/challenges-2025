<?php
if (isset($_GET['pat']) && isset($_GET['rep']) && isset($_GET['sub'])) {
    $pattern = $_GET['pat'];
    $replacement = $_GET['rep'];
    $subject = $_GET['sub'];

    echo "Original : " . htmlspecialchars($subject) . "<br>";
    echo "Replaced : " . preg_replace($pattern, $replacement, $subject);
}
?>

<html>
<head>
    <title>Matcher!</title>
</head>
<body>
    <h2>Enter pattern, replacement, and subject</h2>
    <form action="index.php" method="GET">
        <label for="pat">Pattern:</label>
        <input type="text" id="pat" name="pat"><br><br>

        <label for="rep">Replacement:</label>
        <input type="text" id="rep" name="rep"><br><br>

        <label for="sub">Subject:</label>
        <input type="text" id="sub" name="sub"><br><br>

        <button type="submit">Submit</button>
    </form>
</body>
</html>
