<?php
$initial=$_GET["initial"];
$query = <<<QUERY
SELECT DISTINCT cantonese.reading, cantonese.toneless FROM cantonese, glyph
                      WHERE cantonese.codepoint = glyph.codepoint
                       AND cantonese.initial = ? AND glyph.occurrence
                       ORDER BY cantonese.toneless, cantonese.tone
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($initial));
$rows = $stmt->fetchAll();
$db=null;
$cantoneseInitialList = array();
foreach($rows as $row){
$reading = $row['reading'];
$toneless = $row['toneless'];
$readingsDict = array();
$readingsDict['reading'] = $reading;
$readingsDict['toneless'] = $toneless;
array_push($cantoneseInitialList,$readingsDict);
}
include 'top.php';
$text = <<<TEXT
<h2 class="text">Cantonese</h2>
TEXT;
echo $text;
$oldToneless = "";
foreach($cantoneseInitialList as $key=>$readingsDict){
$reading = $readingsDict['reading'];
$toneless = $readingsDict['toneless'];
if($readingsDict['toneless'] != $oldToneless){
$oldToneless = $toneless;
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
       <a href="../../eohan/cantonese/
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
}
$text = <<<TEXT
</tr></table></td></tr></table>
TEXT;
echo $text;
include 'bottom.php';
?>