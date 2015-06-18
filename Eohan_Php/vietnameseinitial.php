<?php
$initial=$_GET["initial"];
$query = <<<QUERY
SELECT DISTINCT vietnamese.reading, vietnamese.initial, vietnamese.second FROM vietnamese, glyph 
                       WHERE vietnamese.codepoint = glyph.codepoint 
                       AND vietnamese.initial = ? AND glyph.occurrence = 1 
                       ORDER BY vietnamese.initial, vietnamese.second, vietnamese.reading 
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($initial));
$rows = $stmt->fetchAll();
$db=null;
$vietnameseInitialList = array();
foreach($rows as $row){
$reading = $row['reading'];
$initial = $row['initial'];
$second = $row['second'];
$readingsDict = array();
$readingsDict['reading'] = $reading;
$readingsDict['initial'] = $initial;
$readingsDict['second'] = $second;
array_push($vietnameseInitialList,$readingsDict);
}
include 'top.php';
$text = <<<TEXT
<h2 class="text">Vietnamese</h2>
TEXT;
echo $text;
$oldSecond = "£££";
foreach($vietnameseInitialList as $key=>$readingsDict){
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
       <a href="../../eohan/vietnamese/
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