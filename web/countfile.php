<?php
    session_start();
    $count = 0;
    if(isset($_GET['count']))
    {
        $count = $_GET['count'];
        $_SESSION['count'] = $count;
    }else
    {
        if(isset($_SESSION['count']))
        {
            $count = $_SESSION['count'];
        }
    }
    echo $count;
?>