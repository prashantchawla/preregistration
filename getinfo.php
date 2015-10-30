<?php

error_reporting(E_ERROR | E_PARSE);

$course = strtoupper( $_GET['c'] );
$oarsinfourl = "http://oars.cc.iitk.ac.in:4040/Utils/CourseInfoPopup.asp?Course=";

$read_local = file_get_contents('info/'.$course.'.txt');
if( $read_local == FALSE )
{
	$html = new DOMDocument();
	$html->loadHTMLFile($oarsinfourl.$course);

	$table = $html->getElementsByTagName('table');

	if ($table->length == 0) {
		echo 'ERROR!';
	}
	else{
		$table = $html->getElementsByTagName('table')->item(0);
		file_put_contents('info/'.$course.'.txt', $html->saveHTML($table));
		echo $html->saveHTML($table);
	}
}
else 
{
	echo $read_local;
}

?>
