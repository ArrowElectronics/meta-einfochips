<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: text/event-stream');
header('Cache-Control: no-cache');
 header('Content-type: application/json');

$filename = "/usr/share/apache2/htdocs/zclresponse.log";

while(true)
{
  $LastMod = filemtime($filename);
  clearstatcache();
  if(($LastMod + 20) > time())
  {
     $file = read_last_line($filename);
     echo $file;
     break;
  }
else{
    $file = read_last_line($filename);
    echo $file;
    flush();
    break;
   }
}

function read_last_line ($file_path){


$line = '';

$f = fopen($file_path, 'r');
$cursor = -1;
fseek($f, $cursor, SEEK_END);
$char = fgetc($f);

/**
* Trim trailing newline chars of the file
*/

while ($char === "\n" || $char === "\r") {

    fseek($f, $cursor--, SEEK_END);
    $char = fgetc($f);

}

/**
* Read until the start of file or first newline char
*/

while ($char !== false && $char !== "\n" && $char !== "\r") {
    $line = $char . $line;

    fseek($f, $cursor--, SEEK_END);
    $char = fgetc($f);

}

return $line;
}
?>
