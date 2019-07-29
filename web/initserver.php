<?php
    $uploadPath = dirname(__FILE__);
    //清空文件夹函数和清空文件夹后删除空文件夹函数的处理
    function deldir($path){
     //如果是目录则继续
     if(is_dir($path)){
      //扫描一个文件夹内的所有文件夹和文件并返回数组
     $p = scandir($path);
     foreach($p as $val){
      //排除目录中的.和..
      if($val !="." && $val !="..")
      {
       //如果是目录则递归子目录，继续操作
       $subdir = $path."/".$val;
       echo "test ".$subdir."<br>";
       if(is_dir($subdir)){
        //子目录中操作删除文件夹和文件
        
        deldir($subdir);
        //目录清空后删除空文件夹
        //@rmdir($path.$val.'/');
       }else{
        //如果是文件直接删除
        $filePath = $path."/".$val;
        $fileName = basename($filePath);
        echo "fileName ".$fileName."<br>";
        $pos = stripos($fileName,"jpg");
        
        if ($pos)
        {
            echo "delte file " . $filePath . " pos:".$pos . "<br>";
            unlink($filePath) ;
        }
       }
      }
     }
    }
    }
   //调用函数，传入路径
   deldir($uploadPath);
?>