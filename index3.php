<?php
$input = fopen("../../crypto-helper/server.js" , "r");
while(!feof($input)){
    echo fgets($input)."<br>";
}
fclose($input);
?>