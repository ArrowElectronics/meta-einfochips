<?php
 header('Access-Control-Allow-Origin: *');
 header('Content-type: application/json');

$file = fopen("/usr/share/apache2/htdocs/devicejoined.log", "r") or die("Unable to open file!");
// Output one line until end-of-file

$first = "[";

while(! feof($file))
{
//  $lines = COUNT(FILE($file));

  $first= $first.fgets($file);

  $first= $first.",";
}


$first = str_replace(",,", "", $first);

$first = $first."\r";

$first = $first."]";

echo $first;

#fclose($file);
#$jsonData = json_encode($tempArray);
#echo json_encode($first);
fclose($file);
?>
