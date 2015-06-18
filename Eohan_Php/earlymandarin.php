<?php
$reading=$_GET["reading"];
$query = <<<QUERY 
SELECT * FROM 
                        ( 
                    SELECT * FROM 
                    (
                    SELECT em.codepoint, em.glyph, mc.lmc AS reading, 'lmc' AS period FROM 
                    (SELECT * FROM zhongyuanyinyun, earlymandarin WHERE zhongyuanyinyun.homophone = earlymandarin.id) em 
                    LEFT JOIN (SELECT * FROM guangyun, gyhomophone, yunjing 
                    WHERE guangyun.homophone = gyhomophone.id and gyhomophone.yunjing = yunjing.id) mc 
                    ON em.glyph = mc.glyph WHERE em.reading = ? 
                    UNION ALL 
                    SELECT em.codepoint, em.glyph, mc.emc AS reading, 'emc' AS period FROM 
                    (SELECT * FROM zhongyuanyinyun, earlymandarin WHERE zhongyuanyinyun.homophone = earlymandarin.id) em 
                    LEFT JOIN 
                    (SELECT * FROM guangyun, gyhomophone 
                    WHERE guangyun.homophone = gyhomophone.id) mc 
                    ON em.codepoint = mc.codepoint WHERE em.reading = ? 
                    UNION ALL 
                    SELECT em.codepoint, em.glyph, mc.mcb AS reading, 'mcb' AS period FROM 
                    (SELECT * FROM zhongyuanyinyun, earlymandarin WHERE zhongyuanyinyun.homophone = earlymandarin.id) em  
                    LEFT JOIN 
                    (SELECT * FROM guangyun, gyhomophone 
                    WHERE guangyun.homophone = gyhomophone.id) mc 
                    ON em.codepoint = mc.codepoint WHERE em.reading = ? 
                    UNION ALL 
                    SELECT em.codepoint, em.glyph, mc.mck AS reading, 'mck' AS period FROM 
                    (SELECT * FROM zhongyuanyinyun, earlymandarin WHERE zhongyuanyinyun.homophone = earlymandarin.id) em  
                    LEFT JOIN 
                    (SELECT * FROM guangyun, gyhomophone 
                    WHERE guangyun.homophone = gyhomophone.id) mc 
                    ON em.codepoint = mc.codepoint WHERE em.reading = ? 
                    UNION ALL 
                    SELECT em.codepoint, em.glyph, gsr.pulleyblank AS reading, 'ocp' AS period FROM 
                    (SELECT * FROM zhongyuanyinyun, earlymandarin WHERE zhongyuanyinyun.homophone = earlymandarin.id) em  
                    LEFT JOIN gsr 
                    ON em.codepoint = gsr.codepoint WHERE em.reading = ? 
                    UNION ALL 
                    SELECT em.codepoint, em.glyph, gsr.baxter AS reading, 'ocb' AS period FROM 
                    (SELECT * FROM zhongyuanyinyun, earlymandarin WHERE zhongyuanyinyun.homophone = earlymandarin.id) em  
                    LEFT JOIN gsr 
                    ON em.codepoint = gsr.codepoint WHERE em.reading = ? 
                    ) AS readings , glyph 
                    WHERE readings.codepoint = glyph.codepoint AND glyph.occurrence = 1 
                    ORDER BY readings.glyph, readings.period, readings.reading 
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($reading,$reading,$reading,$reading,$reading,$reading)); 
$rows = $stmt->fetchAll();
$db=null;

$emDict = array();
foreach($rows as $row){
$codepoint = $row[0];
$glyph = $row[1];
if(!key_exists($codepoint,$cantoneseDict)){
    $emDict[$codepoint] = ["glyph" => $glyph,
                                 "codepoint" => $codepoint,
                                 "em" => $reading,
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
array_push($emDict[$codepoint][$period],$reading);
} // end for

include 'top.php';

$text = <<<TEXT
<h2 class="text" id="glyphheader" align=center>Cantonese</h2>

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
 </tr>
TEXT;
echo $text;

foreach ($emDict as $codepoint => $glypharray){
$glyph = $glypharray['glyph'];
$cantonese = $glypharray['cantonese'];
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

// ******* EARLY MANDARIN *******

$text = <<<TEXT
  <td class="em">
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT
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
