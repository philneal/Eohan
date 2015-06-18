<?php
$series=$_GET["series"];

$query = <<<QUERY
SELECT karlgren.codepoint, karlgren.glyph, karlgren.id, 
                    mandarin.pinyin, '0 mandarin' AS dialect FROM 
                    karlgren, mandarin 
                    WHERE karlgren.codepoint = mandarin.codepoint 
                    AND karlgren.series = ? 
                    UNION ALL 
                    SELECT karlgren.codepoint, karlgren.glyph, karlgren.id, 
                    cantonese.reading, '1 cantonese' AS dialect FROM 
                    karlgren, cantonese 
                    WHERE karlgren.codepoint = cantonese.codepoint 
                    AND karlgren.series = ? 
                    UNION ALL 
                    SELECT karlgren.codepoint, karlgren.glyph, karlgren.id, 
                    em.reading, '2 em' AS dialect FROM 
                    karlgren LEFT JOIN 
                    (SELECT * FROM zhongyuanyinyun, earlymandarin 
                    WHERE zhongyuanyinyun.homophone = earlymandarin.id) em 
                    WHERE karlgren.codepoint = em.codepoint 
                    AND karlgren.series = ? 
                    UNION ALL 
                    SELECT karlgren.codepoint, karlgren.glyph, karlgren.id, 
                    mc.lmc, '3 lmc' AS dialect FROM 
                    karlgren LEFT JOIN (SELECT * FROM guangyun, gyhomophone, yunjing 
                    WHERE guangyun.homophone = gyhomophone.id and gyhomophone.yunjing = yunjing.id) mc 
                    WHERE karlgren.codepoint = mc.codepoint AND karlgren.series = ? 
                    UNION ALL 
                    SELECT karlgren.codepoint, karlgren.glyph, karlgren.id, 
                    mc.emc, '4 emc' AS dialect FROM 
                    karlgren LEFT JOIN 
                    (SELECT * FROM guangyun, gyhomophone 
                    WHERE guangyun.homophone = gyhomophone.id) mc 
                    WHERE karlgren.codepoint = mc.codepoint AND karlgren.series = ? 
                    UNION ALL 
                    SELECT karlgren.codepoint, karlgren.glyph, karlgren.id, 
                    mc.mcb, '5 mcb' AS dialect FROM 
                    karlgren LEFT JOIN 
                    (SELECT * FROM guangyun, gyhomophone 
                    WHERE guangyun.homophone = gyhomophone.id) mc 
                    WHERE karlgren.codepoint = mc.codepoint AND karlgren.series = ? 
                    UNION ALL 
                    SELECT karlgren.codepoint, karlgren.glyph, karlgren.id, 
                    mc.mck, '6 mck' AS dialect FROM 
                    karlgren LEFT JOIN 
                    (SELECT * FROM guangyun, gyhomophone 
                    WHERE guangyun.homophone = gyhomophone.id) mc 
                    WHERE karlgren.codepoint = mc.codepoint AND karlgren.series = ? 
                    UNION ALL 
                    SELECT karlgren.codepoint, karlgren.glyph, karlgren.id, 
                    gsr.pulleyblank, '7 ocp' AS dialect FROM 
                    karlgren, gsr 
                    WHERE karlgren.codepoint = gsr.codepoint 
                    AND karlgren.series = ? 
                    UNION ALL 
                    SELECT karlgren.codepoint, karlgren.glyph, karlgren.id, 
                    gsr.baxter, '8 ocb' AS dialect FROM 
                    karlgren, gsr 
                    WHERE karlgren.codepoint = gsr.codepoint 
                    AND karlgren.series = ? 
                    ORDER BY karlgren.id, dialect
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($series,$series,$series,$series,$series,$series,$series,$series,$series));
$rows = $stmt->fetchAll();
$db=null;
$karlgrenDict = [];
foreach($rows as $row){
$codepoint = $row[0];
$glyph = $row[1];
if(!key_exists($codepoint,$karlgrenDict)){
$karlgrenDict[$codepoint] = ["glyph" => $glyph,
               "codepoint" => $codepoint,
			   "mandarin" => [],
			   "cantonese" => [],
               "em" => [],
               "lmc" => [],
               "emc" => [],
               "mcb" => [],
               "mck" => [],
               "ocp" => [],
               "ocb" => [],
               "ock" => [],
                 ];
}
}
include 'top.php';
foreach($rows as $row){
$codepoint = $row[0];
$reading = $row[3];
$period = $row[4];
$period = substr($period,2);
array_push($karlgrenDict[$codepoint][$period],$reading);
}
$text = <<<TEXT
<h2 class="text">Analytic Dictionary</h2>

<table class="outerreading">
<tr>
<th class="readingglyph"></th>
<th class="mandarin">Mand</th>
<th class="em">EM</th>
<th class="cantonese">Cant</th>
<th class="lmc">LMC</th>
<th class="emc">EMC</th>
<th class="mcb">MCB</th>
<th class="mck">MCK</th>
<th class="ocp">OCP</th>
<th class="ocb">OCB</th></tr>


TEXT;
echo $text;
foreach($karlgrenDict as $row){
$text = <<<TEXT

<tr>
<td class="readingglyph">
<a href="../../glyph/
TEXT;
echo $text;
echo $row["codepoint"];
$text = <<<TEXT
/">

TEXT;
echo $text;
echo $row["glyph"];
$text = <<<TEXT

</a>
</td>

<td class="mandarin">
<table class="innerreading">

TEXT;
echo $text;
foreach($row["mandarin"] as $mandarin){
$text = <<<TEXT

<tr><td>
TEXT;
echo $text;
$mandarin = str_replace("None","",$mandarin);
echo $mandarin;
$text = <<<TEXT
</td></tr>

TEXT;
echo $text;
}
$text = <<<TEXT

</table>
</td>

<td class="em">
<table class="innerreading">

TEXT;
echo $text;
foreach($row["em"] as $em){
$text = <<<TEXT

<tr><td>
TEXT;
echo $text;
$em = str_replace("None","",$em);
echo $em;
$text = <<<TEXT
</td></tr>

TEXT;
echo $text;
}
$text = <<<TEXT

</table>
</td>

<td class="cantonese">
<table class="innerreading">

TEXT;
echo $text;
foreach($row["cantonese"] as $cantonese){
$text = <<<TEXT

<tr><td>
TEXT;
echo $text;
$cantonese = str_replace("None","",$cantonese);
echo $cantonese;
$text = <<<TEXT
</td></tr>

TEXT;
echo $text;
}
$text = <<<TEXT

</table>
</td>

<td class="lmc">
<table class="innerreading">

TEXT;
echo $text;
foreach($row["lmc"] as $lmc){
$text = <<<TEXT

<tr><td>
TEXT;
echo $text;
$lmc = str_replace("None","",$lmc);
echo $lmc;
$text = <<<TEXT
</td></tr>

TEXT;
echo $text;
}
$text = <<<TEXT

</table>
</td>

<td class="emc">
<table class="innerreading">

TEXT;
echo $text;
foreach($row["emc"] as $emc){
$text = <<<TEXT

<tr><td>
TEXT;
echo $text;
$emc = str_replace("None","",$emc);
echo $emc;
$text = <<<TEXT
</td></tr>

TEXT;
echo $text;
}
$text = <<<TEXT

</table>
</td>

<td class="mcb">
<table class="innerreading">

TEXT;
echo $text;
foreach($row["mcb"] as $mcb){
$text = <<<TEXT

<tr><td>
TEXT;
echo $text;
$mcb = str_replace("None","",$mcb);
echo $mcb;
$text = <<<TEXT
</td></tr>

TEXT;
echo $text;
}
$text = <<<TEXT

</table>
</td>

<td class="mck">
<table class="innerreading">

TEXT;
echo $text;
foreach($row["mck"] as $mck){
$text = <<<TEXT

<tr><td>
TEXT;
echo $text;
$mck = str_replace("None","",$mck);
echo $mck;
$text = <<<TEXT
</td></tr>

TEXT;
echo $text;
}
$text = <<<TEXT

</table>
</td>

<td class="ocp">
<table class="innerreading">

TEXT;
echo $text;
foreach($row["ocp"] as $ocp){
$text = <<<TEXT

<tr><td>
TEXT;
echo $text;
$ocp = str_replace("None","",$ocp);
echo $ocp;
$text = <<<TEXT
</td></tr>

TEXT;
echo $text;
}
$text = <<<TEXT

</table>
</td>

<td class="ocb">
<table class="innerreading">

TEXT;
echo $text;
foreach($row["ocb"] as $ocb){
$text = <<<TEXT

<tr><td>
TEXT;
echo $text;
$ocb = str_replace("None","",$ocb);
echo $ocb;
$text = <<<TEXT
</td></tr>

TEXT;
echo $text;
}
$text = <<<TEXT

</table>
</td>


TEXT;
echo $text;
}
$text = <<<TEXT


</table>


TEXT;
echo $text;
include 'bottom.php';

