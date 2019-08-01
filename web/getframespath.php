<?php

function getFileAmount($face)
{
    $faceDir = "faceimg/".$face."/";
    $jpgFiles = glob($faceDir."*.jpg");
    $fileCount = count($jpgFiles);
    return $fileCount-1;
}

$facesAmount = [];
$facesAmount[0] = getFileAmount("front");
$facesAmount[1] = getFileAmount("back");
$facesAmount[2] = getFileAmount("left");
$facesAmount[3] = getFileAmount("right");
$facesAmount[4] = getFileAmount("top");

echo join(",",$facesAmount )
?>