<?php

$course = strtoupper( $_GET['c'] );

echo file_get_contents('tsvs/'.$course.'.tsv');

?>
