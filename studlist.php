<?php

error_reporting(E_ERROR | E_PARSE);

$course = strtoupper( $_GET['course'] );
$sem = strtoupper( $_GET['sem'] );
$yr = strtoupper( $_GET['yr'] );

$read_local = file_get_contents('tsvs/students/Y'.$yr.'/TSV/'.$course.$sem.'.tsv');
if( $read_local == FALSE )
{
	$txt = $course."\t".$sem."\t".$yr;
	$myfile = file_put_contents('error.txt', $txt.PHP_EOL , FILE_APPEND);
}
else 
{
	echo $read_local;
}

?>
