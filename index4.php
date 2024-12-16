<?php
$input = fopen("../../my_own_cryptographic_algorithm" , "r");
while(!feof($input)){
    echo fgets($input)."<br>";
}
fclose($input);
?>