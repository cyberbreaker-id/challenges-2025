<?php
ini_set('display_errors', 'Off'); error_reporting(0);
if(isset($_GET['file'])) {
    $file = str_replace("../", "", $_GET['file']);
    if($file){
        echo file_get_contents('./files/' . $file);
    }
}else{
    echo file_get_contents('files/welcome.txt');
}

?>