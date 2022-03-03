<?php
header('Access-Control-Allow-Origin: *');
#header('Content-type: application/json');
header("Content-Type: application/json; charset=UTF-8");


$filename = "/usr/share/apache2/htdocs/zigbee/lightinfo.json";
$json = $_POST['json'];


$data = json_decode($json). "\n";
$file = fopen($filename,'w+');
echo $data;
fwrite($file,$json);
fclose($file);

echo 'Success?';

?>
