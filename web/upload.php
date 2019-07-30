<?php
$face = $_POST["face"];
$uploadDir = "uploadimg/".$face."/";
$jpgFiles = glob($uploadDir."*.jpg");
$fileCount = count($jpgFiles)+1;
$uploadFile = $uploadDir . $fileCount.".jpg";
echo $uploadFile;
move_uploaded_file($_FILES["file"]["tmp_name"],$uploadFile);
?>