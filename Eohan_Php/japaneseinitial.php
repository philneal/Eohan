<?php
$initial=$_GET["initial"];
$query = <<<QUERY
SELECT DISTINCT japaneseon.reading, japaneseon.initial, japaneseon.second FROM japaneseon, glyph 
                       WHERE japaneseon.codepoint = glyph.codepoint 
                       AND japaneseon.initial = ? AND glyph.occurrence = 1 
                       ORDER BY japaneseon.initial, japaneseon.second, japaneseon.reading 
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($initial));
$rows = $stmt->fetchAll();
$db=null;
$japaneseInitialList = array();
foreach($rows as $row){
$reading = $row['reading'];
$initial = $row['initial'];
$second = $row['second'];
$readingsDict = array();
$readingsDict['reading'] = $reading;
$readingsDict['initial'] = $initial;
$readingsDict['second'] = $second;
array_push($japaneseInitialList,$readingsDict);
}
include 'top.php';
$text = <<<TEXT
<h2 class="text">Japanese</h2>
TEXT;
echo $text;
$oldSecond = "£££";
foreach($japaneseInitialList as $key=>$readingsDict){
$reading = $readingsDict['reading'];
$initial = $readingsDict['initial'];
$second = $readingsDict['second'];
if($readingsDict['second'] != $oldSecond){
$oldSecond = $second;
if($key==0){
$text = <<<TEXT
<table class="outersyllable">
 <tr class="outersyllable">
  <td class="outersyllable">
    <table class="innersyllable">
     <tr class="innersyllable">
TEXT;
echo $text;
} else {
$text = <<<TEXT
    </tr>                        
   </table>                      
  </td>                          
 </tr>                           
 <tr class="outersyllable">      
  <td class="outersyllable">     
   <table class="innersyllable"> 
    <tr class="innersyllable">   
TEXT;
echo $text;
}
}
$text = <<<TEXT
      <td class="innersyllable">
       <a href="../../eohan/japanese/
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT
	   ">
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT
       </a>
      </td>
TEXT;
echo $text;
}
$text = <<<TEXT
</tr></table></td></tr></table>
TEXT;
echo $text;
include 'bottom.php';
?>