<?php

$input = fopen("../index.php" , "r");
while(!feof($input)){
    echo fgets($input)."<br>";
}
fclose($input);


?>
