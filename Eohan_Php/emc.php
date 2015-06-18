<?php
$reading=$_GET["reading"];
$query = <<<QUERY
SELECT * FROM 
        (SELECT emc.codepoint, emc.glyph, em.reading 
        AS reading, 'em' AS period 
        FROM (SELECT * FROM guangyun, gyhomophone 
        WHERE guangyun.homophone = gyhomophone.id ) emc 
        LEFT JOIN (SELECT * FROM zhongyuanyinyun, earlymandarin 
        WHERE zhongyuanyinyun.homophone = earlymandarin.id) em 
        ON emc.codepoint = em.codepoint 
        WHERE emc.emc = ? 
        UNION ALL 
        SELECT emc.codepoint, emc.glyph, emc.lmc 
        AS reading, 'lmc' AS period 
        FROM (SELECT * FROM guangyun, gyhomophone, yunjing 
        WHERE guangyun.homophone = gyhomophone.id 
        AND gyhomophone.yunjing = yunjing.id) emc 
        WHERE emc.emc = ? 
        UNION ALL 
        SELECT emc.codepoint, emc.glyph, emc.mcb 
        AS reading, 'mcb' AS period 
        FROM (SELECT * FROM guangyun, gyhomophone 
        WHERE guangyun.homophone = gyhomophone.id ) emc 
        WHERE emc.emc = ? 
        UNION ALL 
        SELECT emc.codepoint, emc.glyph, emc.mck 
        AS reading, 'mck' AS period 
        FROM (SELECT * FROM guangyun, gyhomophone 
        WHERE guangyun.homophone = gyhomophone.id ) emc 
        WHERE emc.emc = ? 
        UNION ALL 
        SELECT emc.codepoint, emc.glyph, gsr.pulleyblank 
        AS reading, 'ocp' AS period 
        FROM (SELECT * FROM guangyun, gyhomophone 
        WHERE guangyun.homophone = gyhomophone.id ) emc 
        LEFT JOIN gsr ON emc.codepoint = gsr.codepoint 
        WHERE emc.emc = ? 
        UNION ALL SELECT emc.codepoint, emc.glyph, gsr.baxter 
        AS reading, 'ocb' AS period 
        FROM (SELECT * FROM guangyun, gyhomophone 
        WHERE guangyun.homophone = gyhomophone.id ) emc 
        LEFT JOIN gsr ON emc.codepoint = gsr.codepoint 
        WHERE emc.emc = ? 
        UNION ALL SELECT emc.codepoint, emc.glyph, gsr.karlgren 
        AS reading, 'ock' AS period 
        FROM (SELECT * FROM guangyun, gyhomophone 
        WHERE guangyun.homophone = gyhomophone.id ) emc 
        LEFT JOIN gsr ON emc.codepoint = gsr.codepoint 
        WHERE emc.emc = ? ) AS readings , glyph 
        WHERE readings.codepoint = glyph.codepoint 
        AND glyph.occurrence = 1 
        ORDER BY readings.glyph, readings.period, readings.reading
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($reading,$reading,$reading,$reading,$reading,$reading,$reading)); 
$rows = $stmt->fetchAll();
$db=null;
$emcReading = $reading;

$emcDict = array();
foreach($rows as $row){
$codepoint = $row[0];
$glyph = $row[1];
if(!key_exists($codepoint,$emcDict)){
    $emcDict[$codepoint] = ["glyph" => $glyph,
                                 "codepoint" => $codepoint,
                                 "em" => [],
                                 "lmc" => [],
                                 "emc" => [],
                                 "mcb" => [],
                                 "mck" => [],
                                 "ocp" => [],
                                 "ocb" => [],
                                 "ock" => [],
                                 ];
} // end if
} // end for
foreach($rows as $row){
$codepoint = $row[0];
$reading = $row[2];
$period = $row[3];
array_push($emcDict[$codepoint][$period],$reading);
} // end for

include 'top.php';

$text = <<<TEXT
<h2 class="text" id="glyphheader" align=center>Early Middle Chinese</h2>

<table class="outerreading">
 <tr>
  <th class="readingglyph"></th>
  <th class="em">EM</th>
  <th class="lmc">LMC</th>
  <th class="emc">EMC</th>
  <th class="mcb">MCB</th>
  <th class="mck">MCK</th>
  <th class="ocp">OCP</th>
  <th class="ocb">OCB</th>
  <th class="ock">OCK</th>
 </tr>
TEXT;
echo $text;

foreach ($emcDict as $codepoint => $glypharray){
$glyph = $glypharray['glyph'];
$em = $glypharray['em'];
$lmc = $glypharray['lmc'];
$emc = $glypharray['emc'];
$mcb = $glypharray['mcb'];
$mck = $glypharray['mck'];
$ocp = $glypharray['ocp'];
$ocb = $glypharray['ocb'];
$ock = $glypharray['ock'];

$text = <<<TEXT
 <tr>
  <td class="readingglyph">
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
  </td>
TEXT;
echo $text; 

// ******* EARLY MANDARIN *******

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
  <td class="lmc">
TEXT;
echo $text;
echo $emcReading;
$text = <<<TEXT
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

// ******* OCK *******

$text = <<<TEXT

  <td class="ock">
   <table class="innerreading">
TEXT;
echo $text;
foreach ($ock as $reading){
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