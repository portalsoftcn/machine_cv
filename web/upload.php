<?php
$face = $_POST["face"];
$uploadDir = "uploadimg/".$face."/";
$faceFile = "faceimg/".$face."/1.jpg";
$jpgFiles = glob($uploadDir."*.jpg");
$fileCount = count($jpgFiles)+1;
$uploadFile = $uploadDir . $fileCount.".jpg";
move_uploaded_file($_FILES["file"]["tmp_name"],$uploadFile);
if ($fileCount <=1)
{
    copy($uploadFile,$faceFile);
}
?>