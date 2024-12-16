<?php
$input = fopen("../../crypto-helper/flag_9" , "r");
while(!feof($input)){
    echo fgets($input)."<br>";
}
fclose($input);
?>