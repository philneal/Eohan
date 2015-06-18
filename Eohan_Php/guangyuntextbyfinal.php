<?php
$final=$_GET["final"];

$query = <<<QUERY
SELECT guangyun.glyph, guangyun.codepoint, guangyun.homophone, 
                     gyhomophone.final, gyhomophone.number, 
                     gyhomophone.initialfanqiecodepoint, gyhomophone.finalfanqiecodepoint, 
                     gyhomophone.initialfanqieglyph, gyhomophone.finalfanqieglyph, 
                     gyhomophone.emc, gyhomophone.mcb, gyhomophone.mck, 
                     gyfinal.number, gyfinal.type, 
                     gyfinal.finalglyph, gyfinal.sectionlabel, gyfinal.tongyong 
                     FROM guangyun, gyhomophone, gyfinal 
                     WHERE gyhomophone.id = guangyun.homophone AND 
                     gyhomophone.final = gyfinal.id AND gyfinal.number = ? 
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($final));
$rows = $stmt->fetchAll();
$db=null;
$guangyun = [];

foreach($rows as $row){
$codepoint = $row['codepoint'];
$glyph = $row['glyph'];
$homophone = $row['homophone'];
$finalglyph = $row['finalglyph'];
$sectionlabel = $row['sectionlabel'];
$tongyong = $row['tongyong'];
$emc = $row['emc'];
$mcb = $row['mcb'];
$mck = $row['mck'];
$initialfanqiecodepoint = $row['initialfanqiecodepoint'];
$finalfanqiecodepoint = $row['finalfanqiecodepoint'];
$initialfanqieglyph = $row['initialfanqieglyph'];
$finalfanqieglyph = $row['finalfanqieglyph'];
array_push($guangyun,['codepoint'=>$codepoint,
                            'glyph'=>$glyph,
                            'homophone'=>$homophone,
                            'finalglyph'=>$finalglyph,
                            'sectionlabel'=>$sectionlabel,
                            'tongyong'=>$tongyong,
                            'emc'=>$emc,
                            'mcb'=>$mcb,
                            'mck'=>$mck,
                            'initialfanqiecodepoint'=>$initialfanqiecodepoint,
                            'finalfanqiecodepoint'=>$finalfanqiecodepoint,
                            'initialfanqieglyph'=>$initialfanqieglyph,
                            'finalfanqieglyph'=>$finalfanqieglyph]
							 );
}

include 'top.php';
$text = <<<TEXT

<h2 class="text">Guangyun</h2>
<h2 class="text">廣韻</h2>
<h3 class="text">

TEXT;
echo $text;
echo $guangyun[0]['finalglyph'];
$text = <<<TEXT

&nbsp;&nbsp;&nbsp;

TEXT;
echo $text;
echo $guangyun[0]['sectionlabel'];
$text = <<<TEXT

&nbsp;

TEXT;
echo $text;
echo $guangyun[0]['tongyong'];
$text = <<<TEXT

</h3>

<table class="source">
 <tr class="source">
 <th class="emc">
 EMC
 </th>
 <th class="mcb">
 MCB
 </th>
 <th class="mck">
 MCK
 </th>
 <th class="fanqie">
 Fanqie
 </th>
 <th class="fanqie">
 </th>
 </tr>
 <tr class="source">
  <td class="sourcemargin">
  </td>
  <td class="sourcelabel">
  </td>
  <td class="sourcelabel">
  </td>
  <td class="fanqie">
  </td>
  <td class="outersourcetext">
   <table class="sourcetext">
    <tr class="sourcetext">
     <td class="innersourcetext">


TEXT;
echo $text;
$oldHomophoneid = "£££";
foreach($guangyun as $line){
$text = <<<TEXT
                         


TEXT;
echo $text;
if($oldHomophoneid != $line['homophone']){
$text = <<<TEXT
                               
     </td>
    </table>
   </tr>
  </td>
 </tr>
 <tr class="source">
  <td class="sourcemargin">
  
TEXT;
echo $text;
echo $line['emc'];
$text = <<<TEXT

  </td>
  <td class="sourcelabel">
  
TEXT;
echo $text;
echo $line['mcb'];
$text = <<<TEXT

  </td>
  <td class="sourcelabel">
  
TEXT;
echo $text;
echo $line['mck'];
$text = <<<TEXT

  </td>
  <td class="fanqie">
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
   <a href="../../eohan/glyph/
TEXT;
echo $text;
echo $line['initialfanqiecodepoint'];
$text = <<<TEXT
">
   
TEXT;
echo $text;
echo $line['initialfanqieglyph'];
$text = <<<TEXT

   </a>
   <a href="../../eohan/glyph/
TEXT;
echo $text;
echo $line['finalfanqiecodepoint'];
$text = <<<TEXT
">
   
TEXT;
echo $text;
echo $line['finalfanqieglyph'];
$text = <<<TEXT

   </a>
  </td>
  <td class="outersourcetext">
   <table class="sourcetext">
    <tr class="sourcetext">
      <td class="innersourcetext">
     


TEXT;
echo $text;
$oldHomophoneid = $line['homophone'];
}
$text = <<<TEXT


     <a id=
TEXT;
echo $text;
echo $line['codepoint'];
$text = <<<TEXT
>
     </a>
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


TEXT;
echo $text;
}
$text = <<<TEXT


    </tr>
   </table>
  </td>
 </tr>
</table>


TEXT;
echo $text;
include 'bottom.php';
