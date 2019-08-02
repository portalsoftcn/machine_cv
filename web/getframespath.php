<?php

/*
function getFileAmount($face)
{
    $faceDir = "faceimg/".$face."/";
    $jpgFiles = glob($faceDir."*.jpg");
    $fileCount = count($jpgFiles);
    return $fileCount-1;
}
*/

$facesAmount = [];
$result = "";
$before = time();
for($i = 0;$i<1000;$i++)
{
    $facesAmount[0] = getFileAmount("front");
    $facesAmount[1] = getFileAmount("back");
    $facesAmount[2] = getFileAmount("left");
    $facesAmount[3] = getFileAmount("right");
    $facesAmount[4] = getFileAmount("top");
    $result = join(",",$facesAmount );
}
#echo $result;

$curr = time();

echo $curr - $before;

?>