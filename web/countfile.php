<?php
    $count = 0;
    $fileName = "count.txt";
    if(isset($_GET['count']))
    {
        $count = $_GET['count'];
        $file = fopen($fileName,'w');
        @fwrite($file,$count);
        fclose($file);
    }else
    {
        $fileLength = filesize($fileName);
        if($fileLength>0)
        {
            $file = fopen($fileName,"r");
            $count = fread($file,filesize($fileName));
            fclose($file);
        }else
        {
            $count = 0;
        }
    }
    echo $count;
?>