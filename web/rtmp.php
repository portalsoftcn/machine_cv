<?php ?>

<html> 
<head> 
<title>Live</title> 
<meta charset="utf-8"> 
<link href="http://vjs.zencdn.net/5.5.3/video-js.css" rel="stylesheet"> 
<!-- If you'd like to support IE8 --> 
<script src="http://vjs.zencdn.net/ie8/1.1.1/videojs-ie8.min.js">
</script> 
<script src="http://vjs.zencdn.net/5.5.3/video.js">
</script> 

<style type="text/css">
  table{ border-collapse:collapse; border:solid 1px Black; }
  table td{  border:solid 1px Black; padding:5px;}
  table tr{ align:"center" ;valign:"middle" }
</style>

</head> 
<body style="margin-top: 0px; margin-left:0px;"> 
<table width="1200" height="900" >
  <tr >
    <td>&nbsp;</td>
    <td>
      <video id="vidBack" class="video-js" autoplay muted loop width="400" height="300" data-setup="{}"> 
      
        <source src="<?php
          echo "rtmp://47.111.142.84:1931/device/top1";
          ?>" type="rtmp/flv"> 
      
      </video>
     </td>
    <td>&nbsp;</td>
  </tr>

  <tr >
      <td><video id="vidLeft" class="video-js" autoplay muted loop width="400" height="300" data-setup="{}"> 
          <source src="<?php
          echo "rtmp://192.168.1.14:1931/device/left";
          ?>" type="rtmp/flv"> 
          </video></td>
      <td>
        <video id="vidTop" class="video-js" autoplay muted loop width="400" height="300" data-setup="{}"> 
        <source src="<?php
          echo "rtmp://192.168.1.14:1931/device/front";
          ?>" type="rtmp/flv"> 
        </video>
       </td>
      <td><video id="vidRight" class="video-js" autoplay muted loop width="400" height="300" data-setup="{}"> 
          <source src="<?php
          echo "rtmp://192.168.1.14:1931/device/right";
          ?>" type="rtmp/flv"> 
          </video></td>
    </tr>

    <tr >
        <td>&nbsp;</td>
        <td>
          <video id="vidFront" class="video-js" autoplay muted loop width="400" height="300" data-setup="{}"> 
          <source src="<?php
          echo "rtmp://192.168.1.14:1931/device/back";
          ?>" type="rtmp/flv"> 
          </video>
         </td>
        <td>&nbsp;</td>
      </tr>

</table>


</body> 
</html>


