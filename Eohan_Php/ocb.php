<?php
$final=$_GET["final"];
$query = <<<QUERY
SELECT gsr.codepoint, gsr.glyph, pulleyblank, baxter, baxterfinal, emc, mcb 
                   FROM gsr, guangyun, gyhomophone 
                   WHERE gsr.codepoint = guangyun.codepoint 
                   AND guangyun.homophone = gyhomophone.id 
                   AND baxterfinal = ? 
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($final)); 
$rows = $stmt->fetchAll();
$db=null;

$ocbDict = array();
foreach($rows as $row){
$codepoint = $row[0];
$glyph = $row[1];
if(!key_exists($codepoint,$ocbDict)){
    $ocbDict[$codepoint] = ["glyph" => $glyph,
                                 "codepoint" => $codepoint,
                                 "emc" => [],
                                 "mcb" => [],
                                 "ocp" => [],
                                 "ocb" => [],
                                 ];
} // end if
} // end for
foreach($rows as $row){
$codepoint = $row[0];
$glyph = $row[1];
$ocp = $row[2];
$ocb = $row[3];
$emc = $row[5];
$mcb = $row[6];
array_push($ocbDict[$codepoint]['emc'],$emc);
array_push($ocbDict[$codepoint]['mcb'],$mcb);
array_push($ocbDict[$codepoint]['ocp'],$ocp);
array_push($ocbDict[$codepoint]['ocb'],$ocb);
} // end for

include 'top.php';

$text = <<<TEXT
<h2 class="text" id="glyphheader" align=center>Old Chinese: Baxter</h2>

<table class="outerreading">
 <tr>
  <th class="readingglyph"></th>
  <th class="emc">EMC</th>
  <th class="mcb">MCB</th>
  <th class="ocp">OCP</th>
  <th class="ocb">OCB</th>
 </tr>
TEXT;
echo $text;

foreach ($ocbDict as $glypharray){
$codepoint = $glypharray['codepoint'];
$glyph = $glypharray['glyph'];
$emc = $glypharray['emc'];
$mcb = $glypharray['mcb'];
$ocp = $glypharray['ocp'];
$ocb = $glypharray['ocb'];

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

// ******* EMC *******


$text = <<<TEXT

  <td class="mcb">
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
