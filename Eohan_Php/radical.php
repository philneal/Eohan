<?php
$radical=$_GET["radical"];
$query = <<<QUERY
SELECT glyph.codepoint, glyph.glyph, radical.radicalnumber, radical.strokecount FROM radical, glyph 
                    WHERE radical.codepoint = glyph.codepoint 
                    AND glyph.occurrence = 1 AND radical.radicalnumber = ? 
                    ORDER BY radical.radicalnumber, radical.strokecount 
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($radical)); 
$rows = $stmt->fetchAll();
$db=null;

$radicalDict = array();
foreach($rows as $row){
$strokeCount = $row[3];
if(!key_exists($strokeCount,$radicalDict)){
$radicalDict[$strokeCount] = [];
}
}
foreach($rows as $row){
$codepoint = $row[0];
$glyph = $row[1];
$strokeCount = $row[3];
array_push($radicalDict[$strokeCount],['codepoint'=>$codepoint,
                                       'glyph'=>$glyph]);
}

include 'top.php';

$text = <<<TEXT
<h2 class="text">Radical and Strokes</h2>

<table class="source">
TEXT;
echo $text;
foreach($radicalDict as $strokeCount=>$glyphArray){
$text = <<<TEXT
 <tr class="source">
  <td class="sourcemargin">
  &nbsp;
  </td>
 </tr>
 <tr>
  <td class="sourcemargin">
TEXT;
echo $text;
echo $strokeCount;
foreach($glyphArray as $pair){
$codepoint = $pair['codepoint'];
$glyph = $pair['glyph'];
$text = <<<TEXT
  <td class="innersourcetext">
  <a href="../../eohan/glyph/
TEXT;
echo $text;
echo $codepoint;
$text = <<<TEXT
 ">
TEXT;
echo $text;
echo $glyph;
$text = <<<TEXT
  </a>
TEXT;
echo $text;
}
$text = <<<TEXT
  </td>
 </tr>
TEXT;
echo $text;
}
$text = <<<TEXT
</table>
TEXT;
echo $text;

include 'bottom.php';