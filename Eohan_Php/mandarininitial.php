<?php
$initial=$_GET["initial"];
$query = <<<QUERY
SELECT DISTINCT mandarin.pinyin, mandarin.toneless FROM mandarin, glyph
                      WHERE mandarin.codepoint = glyph.codepoint
                       AND mandarin.initial = ? AND glyph.occurrence
                       ORDER BY mandarin.toneless, mandarin.tone, mandarin.pinyin
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($initial));
$rows = $stmt->fetchAll();
$db=null;
$mandarinInitialList = array();
foreach($rows as $row){
$pinyin = $row['pinyin'];
$toneless = $row['toneless'];
$readingsDict = array();
$readingsDict['pinyin'] = $pinyin;
$readingsDict['toneless'] = $toneless;
array_push($mandarinInitialList,$readingsDict);
}
include 'top.php';
$text = <<<TEXT
<h2 class="text">Mandarin</h2>
TEXT;
echo $text;
$oldToneless = "";
foreach($mandarinInitialList as $key=>$readingsDict){
$pinyin = $readingsDict['pinyin'];
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
      <td class="innersyllable">
       <a href="../../mandarintoneless/{{ dict.toneless }}">
TEXT;
echo $text;
echo $toneless;
$text = <<<TEXT
       </a>
      </td>
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
       <a href="../../eohan/mandarin/
TEXT;
echo $text;
echo $pinyin;
$text = <<<TEXT
	   ">
TEXT;
echo $text;
echo $pinyin;
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