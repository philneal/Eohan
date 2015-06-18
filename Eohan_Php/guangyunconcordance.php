<?php
$codepoint=$_GET["codepoint"];

$query = <<<QUERY
SELECT b.codepoint, b.glyph, b.homophonenumber, 
                           b.initialfanqie, b.finalfanqie, b.homophone, b.finalnumber, 
                           b.finalglyph, b.sectionlabel, b.tongyong, b.tonenumber 
                           FROM (SELECT  a1.codepoint AS codepoint, a2.id AS homophone 
                           FROM guangyun AS a1, gyhomophone AS a2, gyfinal AS a3, gytone AS a4 
                           WHERE a1.homophone = a2.id 
                           AND a2.final = a3.id 
                           AND a3.tone = a4.id) a, 
                           (SELECT  b1.id AS id, b1.codepoint AS codepoint, b1.glyph AS glyph, 
                           b2.number AS homophonenumber, b2.initialfanqieglyph AS initialfanqie, 
                           b2.finalfanqieglyph AS finalfanqie, b2.id AS homophone, 
                           b3.id AS final, b3.number AS finalnumber, 
                           b3.finalglyph AS finalglyph, 
                           b3.sectionlabel AS sectionlabel, b3.tongyong AS tongyong, b4.number AS tonenumber 
                           FROM guangyun AS b1, gyhomophone AS b2, gyfinal AS b3, gytone AS b4 
                           WHERE b1.homophone = b2.id 
                           AND b2.final = b3.id 
                           AND b3.tone = b4.id) b 
                           WHERE a.codepoint = ? 
                           AND a.homophone = b.homophone  
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($codepoint));
$rows = $stmt->fetchAll();
$db=null;
$guangyun = [];

foreach($rows as $row){
$codepoint = $row['b.codepoint'];
$glyph = $row['b.glyph'];
$homophone = $row['b.homophone'];
$finalglyph = $row['b.finalglyph'];
$finalnumber = $row['b.finalnumber'];
$sectionlabel = $row['b.sectionlabel'];
$tongyong = $row['b.tongyong'];
$initialfanqie = $row['b.initialfanqie'];
$finalfanqie = $row['b.finalfanqie'];
array_push($guangyun,['codepoint'=>$codepoint,
                            'glyph'=>$glyph,
                            'homophone'=>$homophone,
                            'finalglyph'=>$finalglyph,
                            'finalnumber'=>$finalnumber,
                            'sectionlabel'=>$sectionlabel,
                            'tongyong'=>$tongyong,
                            'initialfanqie'=>$initialfanqie,
                            'finalfanqie'=>$finalfanqie]
							 );
}

include 'top.php';
$text = <<<TEXT

<h2 class="text">Guangyun</h2>
<h2 class="text">廣韻</h2>

<table class="source">
 <tr class="source">
  <td class="outersourcetext">
   <table class="outersourcetext">
    <tr>
     <td class="sourcemargin">
     </td>
     <td class="sourcelabel">
     </td>
     <td class="sourcelabel">
     </td>
    </tr>
   </table>
  </td>
 </tr>
 <tr class="source">
  <td class="outersourcetext">
   <table class="outersourcetext">
    <tr>
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
       </tr>
      </table>
     </td>
    </tr>
   </table>
  </td>
 </tr>
 <tr class="source">
  <td class="outersourcetext">
   <table class="outersourcetext">
    <tr>
     <td class="sourcemargin">
      <a href= "../guangyuntextbyfinal/
TEXT;
echo $text;
echo $line['finalnumber'];
$text = <<<TEXT
">
      
TEXT;
echo $text;
echo $line['finalnumber'];
$text = <<<TEXT

      </a>
     </td>
     <td class="sourcelabel">
     
TEXT;
echo $text;
echo $line['finalglyph'];
$text = <<<TEXT

     </td>
     <td class="sourcelabel">
     
TEXT;
echo $text;
echo $line['sectionlabel'];
$text = <<<TEXT

     </td>
     <td class="sourcelabel">
     
TEXT;
echo $text;
echo $line['tongyong'];
$text = <<<TEXT

     </td>
    </tr>
   </table>
  </td>
 </tr>
 <tr class="source">
  <td class="outersourcetext">
   <table class="outersourcetext">
    <tr>
     <td class="sourcemargin">
     
TEXT;
echo $text;
echo $line['homophone'];
$text = <<<TEXT

     </td>
     <td class="sourcelabel">
     
TEXT;
echo $text;
echo $line['glyph'];
$text = <<<TEXT

TEXT;
echo $text;
echo $line['initialfanqie'];
$text = <<<TEXT

TEXT;
echo $text;
echo $line['finalfanqie'];
$text = <<<TEXT

     </td>
     <td class="outersourcetext">
      <table class="sourcetext">
       <tr class="sourcetext">
        <td class="innersourcetext">
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
$oldHomophoneid = $line['homophone'];
}
$text = <<<TEXT

        </td>
       </tr>
      </table>
     </td>
    </tr>
   </table>
  </td>
 </tr>
</table>


TEXT;
echo $text;
include 'bottom.php';
