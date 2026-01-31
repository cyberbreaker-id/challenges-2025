<?php

if (isset($_GET['search'])) {
    $search = $_GET['search'];

    $cmd = "find /var/www/html/uploads -type f -iname " . escapeshellcmd($search);
    echo "<pre>";
    system($cmd);
    echo "</pre>";
} else {
    ?>
    <h2>FileVault Search</h2>
    <form method="GET">
        <label>Search term: <input type="text" name="search" /></label>
        <button type="submit">Search</button>
    </form>
    <p>Try searching for things like <code>*.txt</code>.</p>
    <?php
}
?>
