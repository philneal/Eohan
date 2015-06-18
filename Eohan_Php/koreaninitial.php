<?php
$initial=$_GET["initial"];
$query = <<<QUERY
SELECT DISTINCT korean.reading, korean.initial, korean.second FROM korean, glyph 
                       WHERE korean.codepoint = glyph.codepoint 
                       AND korean.initial = ? AND glyph.occurrence = 1 
                       ORDER BY korean.initial, korean.second, korean.reading 
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($initial));
$rows = $stmt->fetchAll();
$db=null;
$koreanInitialList = array();
foreach($rows as $row){
$reading = $row['reading'];
$initial = $row['initial'];
$second = $row['second'];
$readingsDict = array();
$readingsDict['reading'] = $reading;
$readingsDict['initial'] = $initial;
$readingsDict['second'] = $second;
array_push($koreanInitialList,$readingsDict);
}
include 'top.php';
$text = <<<TEXT
<h2 class="text">Korean</h2>
TEXT;
echo $text;
$oldSecond = "£££";
foreach($koreanInitialList as $key=>$readingsDict){
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
       <a href="../../eohan/korean/
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