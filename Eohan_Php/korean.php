<?php
$reading=$_GET["reading"];
$query = <<<QUERY
SELECT * FROM 
                    (
                    SELECT korean.codepoint, korean.glyph, mc.lmc AS reading, 'lmc' AS period FROM 
                    korean 
                    LEFT JOIN (SELECT * FROM guangyun, gyhomophone, yunjing 
                    WHERE guangyun.homophone = gyhomophone.id and gyhomophone.yunjing = yunjing.id) mc 
                    ON korean.glyph = mc.glyph WHERE korean.reading = ? 
                    UNION ALL 
                    SELECT korean.codepoint, korean.glyph, mc.emc AS reading, 'emc' AS period FROM 
                    korean LEFT JOIN 
                    (SELECT * FROM guangyun, gyhomophone 
                    WHERE guangyun.homophone = gyhomophone.id) mc 
                    ON korean.codepoint = mc.codepoint WHERE korean.reading = ? 
                    UNION ALL 
                    SELECT korean.codepoint, korean.glyph, mc.mcb AS reading, 'mcb' AS period FROM 
                    korean 
                    LEFT JOIN 
                    (SELECT * FROM guangyun, gyhomophone 
                    WHERE guangyun.homophone = gyhomophone.id) mc 
                    ON korean.codepoint = mc.codepoint WHERE korean.reading = ? 
                    UNION ALL 
                    SELECT korean.codepoint, korean.glyph, mc.mck AS reading, 'mck' AS period FROM 
                    korean 
                    LEFT JOIN 
                    (SELECT * FROM guangyun, gyhomophone 
                    WHERE guangyun.homophone = gyhomophone.id) mc 
                    ON korean.codepoint = mc.codepoint WHERE korean.reading = ? 
                    ) AS readings , glyph 
                    WHERE readings.codepoint = glyph.codepoint AND glyph.occurrence = 1 
                    ORDER BY readings.glyph, readings.period, readings.reading  
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($reading,$reading,$reading,$reading)); 
$rows = $stmt->fetchAll();
$db=null;

$koreanDict = array();
foreach($rows as $row){
$codepoint = $row[0];
$glyph = $row[1];
if(!key_exists($codepoint,$koreanDict)){
    $koreanDict[$codepoint] = ["glyph" => $glyph,
                                 "codepoint" => $codepoint,
                                 "lmc" => [],
                                 "emc" => [],
                                 "mcb" => [],
                                 "mck" => [],
                                 ];
} // end if
} // end for
$koreanReading = $reading;
foreach($rows as $row){
$codepoint = $row[0];
$reading = $row[2];
$period = $row[3];
array_push($koreanDict[$codepoint][$period],$reading);
} // end for

include 'top.php';

$text = <<<TEXT
<h2 class="text" id="glyphheader" align=center>Korean</h2>

<table class="outerreading">
 <tr>
  <th class="readingglyph"></th>
  <th class="korean">Kor</th>
  <th class="lmc">LMC</th>
  <th class="emc">EMC</th>
  <th class="mcb">MCB</th>
  <th class="mck">MCK</th>
 </tr>
TEXT;
echo $text;

foreach ($koreanDict as $codepoint => $glypharray){
$glyph = $glypharray['glyph'];
$lmc = $glypharray['lmc'];
$emc = $glypharray['emc'];
$mcb = $glypharray['mcb'];
$mck = $glypharray['mck'];

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
  <td class="korean">
TEXT;
echo $text; 
echo $koreanReading;

// ******* LMC *******

$text = <<<TEXT

  </td>
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

$text = <<<TEXT
	 </td></tr>
TEXT;
echo $text;
}

$text = <<<TEXT
</table>
TEXT;
echo $text;
include 'bottom.php';
