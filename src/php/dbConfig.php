<?php

$dbHost     = "localhost";  
$dbUsername = "root";  
$dbPassword = "Terziev123";  
$dbName     = "WBD";

$db = new mysqli($dbHost, $dbUsername, $dbPassword, $dbName);  

if ($db->connect_error) {  
    die("Connection failed: " . $db->connect_error);  
}