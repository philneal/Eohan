<?php
	  if(isset($_POST['submit'])){ 
	  if(isset($_GET['go'])){ 
	  if(preg_match("/\p{Han}/u", $_POST['glyph'])){ 
	  $glyph=$_POST['glyph']; 
	  $db = new PDO('sqlite:database/cp.db');
      $query="SELECT  codepoint, glyph FROM glyph WHERE glyph = ?"; 
      $stmt = $db->prepare($query);
      $stmt->execute([$glyph]);
	  $codepoint = $stmt->fetch()[0];
	  if(strlen(utf8_decode($glyph)) == 1){
	  $url = "Location: ../../eohan/glyph/".$codepoint;
	  } else {
	  $url = "Location: ../../eohan/main";
	  }
      header($url);
	  } else { 
	  $url = "Location: ../../eohan/main";
	  }
      header($url);
	  } 
	  } 
	?>