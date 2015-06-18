<?php
$codepoint=$_GET["codepoint"];

$query = <<<QUERY
SELECT a.glyph, b.id, b.codepoint, b.glyph, 
                           b.phonetic, b.phoneticlabel, b.glyphlabel 
                           FROM (SELECT * FROM gsr WHERE codepoint = ? LIMIT 1) a, gsr b 
                           WHERE a.phonetic = b.phonetic  
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($codepoint));
$rows = $stmt->fetchAll();
$db=null;
$gsr = $rows;

include 'top.php';
$text = <<<TEXT

<h2 class="text">Grammata Serica Recensa</h2>
<h3 class="text">
TEXT;
echo $text;
echo $gsr[0]['phoneticlabel'];
$text = <<<TEXT
</h3>

<table class="source">

TEXT;
echo $text;
$oldCodepoint = $gsr[0]['codepoint'];
foreach($gsr as $line){

if($oldCodepoint != $line['codepoint']){
$oldCodepoint != $line['codepoint'];
$text = <<<TEXT

 <tr>
  <td class="sourcemargin">
  
TEXT;
echo $text;
echo $line['phoneticlabel'];
$text = <<<TEXT

TEXT;
echo $text;
echo $line['glyphlabel'];
$text = <<<TEXT

  </td>           
  <td class="outersourcetext">
   <a href="../../eohan/glyph/
TEXT;
echo $text;
echo $line['codepoint'];
$text = <<<TEXT
">
   
TEXT;
echo $text;
echo $line['glyph'];
$text = <<<TEXT

   </a>
  </td>
 </tr>


TEXT;
echo $text;
}
$text = <<<TEXT


TEXT;
echo $text;
}
$text = <<<TEXT

</table>


 </table>

TEXT;
echo $text;
include 'bottom.php';

