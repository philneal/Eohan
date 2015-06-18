<?php
$rhymerange=$_GET["rhyme"];
$rhymearray=explode("-",$rhymerange);

$query = <<<QUERY
SELECT gsr.id, gsr.codepoint, gsr.glyph, 
                   gsr.phonetic, 
                   gsr.phoneticlabel, gsr.glyphlabel, 
                   gsr.pulleyblank, gsr.baxter, gsr.karlgren, 
                   gyhomophone.emc, gyhomophone.mcb 
                   FROM gsr, gyhomophone 
                   WHERE gsr.gyhomophone = gyhomophone.id 
                   AND gsr.phonetic >= ? 
                   AND gsr.phonetic <= ?
                   ORDER BY gsr.id 
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($rhymearray[0],$rhymearray[1]));
$rows = $stmt->fetchAll();
$db=null;
$gsr = $rows;

include 'top.php';
$text = <<<TEXT

<h2 class="text">Grammata Serica Recensa</h2>

<table class="outerreading">
<tr>
<th class="readingglyph"></th>
<th class="readingglyph"></th>
<th class="emc">EMC</h3></th>
<th class="mcb">MCB</h3></th>
<th class="ocp">OCP</h3></th>
<th class="ocb">OCB</h3></th>
<th class="ocb">OCK</h3></th>
</tr>



TEXT;
echo $text;
$oldPhoneticLabel = $gsr[0]['phoneticlabel'];
$oldLineId = $gsr[0]['id'];
$oldCodepoint = $gsr[0]['codepoint'];
$ctr = 0;
foreach($gsr as $line){
if($oldPhoneticLabel != $line['phoneticlabel']){
$oldPhoneticLabel = $line['phoneticlabel'];
if($ctr != 0){
$text = <<<TEXT

<tr>
<td class="blankreading">&nbsp;</td>
<td class="blankreading">&nbsp;</td>
<td class="blankreading">&nbsp;</td>
<td class="blankreading">&nbsp;</td>
<td class="blankreading">&nbsp;</td>
<td class="blankreading">&nbsp;</td>
<td class="blankreading">&nbsp;</td>
</tr>

TEXT;
echo $text;
}
$ctr++;
}
if($oldLineId != $line['id']){
$oldLineId = $line['id'];
$text = <<<TEXT
<tr>
TEXT;
echo $text;
if($oldCodepoint != $line['codepoint']){
$oldCodepoint != $line['codepoint'];
$text = <<<TEXT

<td class="readingglyph"><a href="../../eohan/glyph/
TEXT;
echo $text;
echo $line['codepoint'];
$text = <<<TEXT
">

TEXT;
echo $text;
echo $line['glyph'];
$text = <<<TEXT

</a></td>


TEXT;
echo $text;
} else {
$text = <<<TEXT

<td class="readingglyph"></td>

TEXT;
echo $text;
}
$text = <<<TEXT
<td class="readingglyph">
TEXT;
echo $text;
echo $line['phoneticlabel'];
$text = <<<TEXT

TEXT;
echo $text;
echo $line['glyphlabel'];
$text = <<<TEXT
</td>           
<td class="emc">
TEXT;
echo $text;
echo $line['emc'];
$text = <<<TEXT
</td>           
<td class="mcb">
TEXT;
echo $text;
echo $line['mcb'];
$text = <<<TEXT
</td>           
<td class="ocp">
TEXT;
echo $text;
echo $line['pulleyblank'];
$text = <<<TEXT
</td>           
<td class="ocb">
TEXT;
echo $text;
echo $line['baxter'];
$text = <<<TEXT
</td>           
<td class="ock">
TEXT;
echo $text;
echo $line['karlgren'];
$text = <<<TEXT
</td>           
</tr>

TEXT;
echo $text;
} else {
$text = <<<TEXT

<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
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

TEXT;
echo $text;
include 'bottom.php';
