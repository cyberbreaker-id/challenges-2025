<?php

error_reporting(0);

if (isset($_GET['file'])) {
    $file = str_replace("../", "", $_GET['file']);

    if (stripos($file, "pearcmd") !== false || stripos($file, "flag") !== false) {
        exit;
    }

    $path = './files/' . $file;
} else {
    $path = 'files/php.txt';
}

if (file_exists($path)) {
    ob_start();
    include($path);
    $output = ob_get_clean();

    if (strpos($output, "CBC") === false) {
        echo $output;
    }
}

?>
