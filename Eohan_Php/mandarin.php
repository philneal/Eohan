<?php
$reading=$_GET["reading"];
$query = <<<QUERY
SELECT * FROM 
                    (
                    SELECT mandarin.codepoint, mandarin.glyph, em.reading AS reading, 'em' AS period FROM 
                    mandarin LEFT JOIN 
                    (SELECT * FROM zhongyuanyinyun, earlymandarin 
                    WHERE zhongyuanyinyun.homophone = earlymandarin.id) em 
                    ON mandarin.codepoint = em.codepoint WHERE mandarin.pinyin = ? 
                    UNION ALL 
                    SELECT mandarin.codepoint, mandarin.glyph, mc.lmc AS reading, 'lmc' AS period FROM 
                    mandarin 
                    LEFT JOIN (SELECT * FROM guangyun, gyhomophone, yunjing 
                    WHERE guangyun.homophone = gyhomophone.id and gyhomophone.yunjing = yunjing.id) mc 
                    ON mandarin.glyph = mc.glyph WHERE mandarin.pinyin = ? 
                    UNION ALL 
                    SELECT mandarin.codepoint, mandarin.glyph, mc.emc AS reading, 'emc' AS period FROM 
                    mandarin LEFT JOIN 
                    (SELECT * FROM guangyun, gyhomophone 
                    WHERE guangyun.homophone = gyhomophone.id) mc 
                    ON mandarin.codepoint = mc.codepoint WHERE mandarin.pinyin = ? 
                    UNION ALL 
                    SELECT mandarin.codepoint, mandarin.glyph, mc.mcb AS reading, 'mcb' AS period FROM 
                    mandarin 
                    LEFT JOIN 
                    (SELECT * FROM guangyun, gyhomophone 
                    WHERE guangyun.homophone = gyhomophone.id) mc 
                    ON mandarin.codepoint = mc.codepoint WHERE mandarin.pinyin = ? 
                    UNION ALL 
                    SELECT mandarin.codepoint, mandarin.glyph, mc.mck AS reading, 'mck' AS period FROM 
                    mandarin 
                    LEFT JOIN 
                    (SELECT * FROM guangyun, gyhomophone 
                    WHERE guangyun.homophone = gyhomophone.id) mc 
                    ON mandarin.codepoint = mc.codepoint WHERE mandarin.pinyin = ? 
                    UNION ALL 
                    SELECT mandarin.codepoint, mandarin.glyph, gsr.pulleyblank AS reading, 'ocp' AS period FROM 
                    mandarin 
                    LEFT JOIN gsr 
                    ON mandarin.codepoint = gsr.codepoint WHERE mandarin.pinyin = ? 
                    UNION ALL 
                    SELECT mandarin.codepoint, mandarin.glyph, gsr.baxter AS reading, 'ocb' AS period FROM 
                    mandarin 
                    LEFT JOIN gsr 
                    ON mandarin.codepoint = gsr.codepoint WHERE mandarin.pinyin = ? 
                    ) AS readings , glyph 
                    WHERE readings.codepoint = glyph.codepoint AND glyph.occurrence = 1 
                    ORDER BY readings.glyph, readings.period, readings.reading 
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($reading,$reading,$reading,$reading,$reading,$reading,$reading)); 
$rows = $stmt->fetchAll();
$db=null;

$mandarinDict = array();
foreach($rows as $row){
$codepoint = $row[0];
$glyph = $row[1];
if(!key_exists($codepoint,$mandarinDict)){
    $mandarinDict[$codepoint] = ["glyph" => $glyph,
                                 "codepoint" => $codepoint,
                                 "mandarin" => $reading,
                                 "em" => [],
                                 "lmc" => [],
                                 "emc" => [],
                                 "mcb" => [],
                                 "mck" => [],
                                 "ocp" => [],
                                 "ocb" => [],
                                 ];
} // end if
} // end for
foreach($rows as $row){
$codepoint = $row[0];
$reading = $row[2];
$period = $row[3];
array_push($mandarinDict[$codepoint][$period],$reading);
} // end for

include 'top.php';

$text = <<<TEXT
<h2 class="text" id="glyphheader" align=center>Mandarin</h2>

<table class="outerreading">
 <tr>
  <th class="readingglyph"></th>
  <th class="mandarin">Mand</th>
  <th class="em">LMC</th>
   <th class="lmc">LMC</th>
  <th class="emc">EMC</th>
  <th class="mcb">MCB</th>
  <th class="mck">MCK</th>
  <th class="ocp">OCP</th>
  <th class="ocb">OCB</th>
 </tr>
TEXT;
echo $text;

foreach ($mandarinDict as $codepoint => $glypharray){
$glyph = $glypharray['glyph'];
$cantonese = $glypharray['mandarin'];
$em = $glypharray['em'];
$lmc = $glypharray['lmc'];
$emc = $glypharray['emc'];
$mcb = $glypharray['mcb'];
$mck = $glypharray['mck'];
$ocp = $glypharray['ocp'];
$ocb = $glypharray['ocb'];

$text = <<<TEXT
 <tr>
  <td class="readingglyph">
   <a href="../../eohan/glyph/
TEXT;
echo $text;
echo urlencode($codepoint);
$text = <<<TEXT
">
TEXT;
echo $text;
echo $glyph;
$text = <<<TEXT
   </a>
  </td>
TEXT;
echo $text; 

// ******* MANDARIN *******

$text = <<<TEXT
  <td class="cantonese">
TEXT;
echo $text;
echo $cantonese;
$text = <<<TEXT
  </td>
TEXT;
echo $text;

// ******* EM *******

$text = <<<TEXT

  <td class="em">
   <table class="innerreading">
TEXT;
echo $text;

foreach ($em as $reading){
$text = <<<TEXT
     <tr><td>
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT
	 </td></tr>
TEXT;
echo $text;
}
$text= <<<TEXT
    </table>
  </td>
TEXT;
echo $text;

// ******* LMC *******

$text = <<<TEXT

  <td class="lmc">
   <table class="innerreading">
TEXT;
echo $text;

foreach ($lmc as $reading){
$text = <<<TEXT
     <tr><td>
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT
	 </td></tr>
TEXT;
echo $text;
}
$text= <<<TEXT
    </table>
  </td>
TEXT;
echo $text;

// ******* EMC *******

$text = <<<TEXT

  <td class="emc">
   <table class="innerreading">
TEXT;
echo $text;
foreach ($emc as $reading){
$text = <<<TEXT
     <tr><td>
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT
	 </td></tr>
TEXT;
echo $text;
}
$text= <<<TEXT
    </table>
  </td>
TEXT;
echo $text;

// ******* MCB *******

$text = <<<TEXT

  <td class="mcb">
   <table class="innerreading">
TEXT;
echo $text;
foreach ($mcb as $reading){
$text = <<<TEXT
     <tr><td>
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT
	 </td></tr>
TEXT;
echo $text;
}
$text= <<<TEXT
    </table>
  </td>
TEXT;
echo $text;

// ******* MCK *******

$text = <<<TEXT

  <td class="mck">
   <table class="innerreading">
TEXT;
echo $text;
foreach ($mck as $reading){
$text = <<<TEXT
     <tr><td>
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT
	 </td></tr>
TEXT;
echo $text;
}
$text= <<<TEXT
    </table>
  </td>
TEXT;
echo $text;

// ******* OCP *******

$text = <<<TEXT

  <td class="ocp">
   <table class="innerreading">
TEXT;
echo $text;
foreach ($ocp as $reading){
$text = <<<TEXT
     <tr><td>
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT
	 </td></tr>
TEXT;
echo $text;
}
$text= <<<TEXT
    </table>
  </td>
TEXT;
echo $text;

// ******* OCB *******

$text = <<<TEXT

  <td class="ocb">
   <table class="innerreading">
TEXT;
echo $text;
foreach ($ocb as $reading){
$text = <<<TEXT
     <tr><td>
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT
	 </td></tr>
TEXT;
echo $text;
}
$text= <<<TEXT
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
?>