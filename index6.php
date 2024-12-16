<?php
$input = fopen("../../../home/passoire/flag_1" , "r");
while(!feof($input)){
    echo fgets($input)."<br>";
}
fclose($input);
?>