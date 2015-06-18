<?php
$codepoint=$_GET["codepoint"];

$query = <<<QUERY
SELECT b.codepoint, b.glyph, b.reading, b.annotation, b.homophonenumber, 
                     b.finallabel, b.rhymelabel, b.rhyme 
                     FROM 
                     (SELECT a1.codepoint AS codepoint, a1.homophone AS homophone 
                      FROM zhongyuanyinyun AS a1, earlymandarin AS a2 
                      WHERE a1.homophone = a2.id) a, 
                     (SELECT b1.id AS id, b1.codepoint AS codepoint, b1.glyph AS glyph, 
                      b1.homophone AS homophone, b1.annotation AS annotation, 
                      b2.reading AS reading, 
                      b3.id AS homophoneid, b3.number AS homophonenumber, 
                      b4.label AS finallabel, b5.number AS rhyme, b5.label AS rhymelabel 
                      FROM zhongyuanyinyun AS b1, earlymandarin AS b2, zyhomophone AS b3, zyfinal AS b4, zyrhyme AS b5 
                      WHERE b1.homophone = b2.id AND b1.homophone = b3.id AND b3.final = b4.id AND b4.rhyme = b5.id) b 
                     WHERE a.codepoint = ? 
                     AND a.homophone = b.homophone 
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($codepoint));
$rows = $stmt->fetchAll();
$db=null;
$zhongyuanYinyun = [];

foreach($rows as $row){
$codepoint = $row['b.codepoint'];
$glyph = $row['b.glyph'];
$reading = $row['b.reading'];
$annotation = $row['b.annotation'];
$homophone = $row['b.homophonenumber'];
$final = $row['b.finallabel'];
$rhymeLabel = $row['b.rhymelabel'];
$rhyme = $row['b.rhyme'];
array_push($zhongyuanYinyun,['codepoint'=>$codepoint,
                            'glyph'=>$glyph,
                            'reading'=>$reading,
                            'annotation'=>$annotation,
                            'homophone'=>$homophone,
                            'final'=>$final,
                            'rhymelabel'=>$rhymeLabel,
                            'rhyme'=>$rhyme]
							 );
}

include 'top.php';
$text = <<<TEXT

<h2 class="text">Zhongyuan Yinyun</h2>
<h2 class="text">中原音韻</h2>

<table class="source">
 <tr class="source">
  <td class="sourcemargin">
  </td>
  <td class="sourcelabel">
  </td>
  <td class="sourcelabel">
  </td>
  <td class="outersourcetext">
   <table class="sourcetext">
    <tr class="sourcetext">


TEXT;
echo $text;
$oldFinal = "£££";
$oldHomophone = "£££";
$oldReading = "£££";
$oldAnnotation = "";
foreach($zhongyuanYinyun as $line){

$text = <<<TEXT
                         


TEXT;
echo $text;
$homophone = $line['homophone'];
if($homophone != $oldHomophone){
$text = <<<TEXT
                          
    </tr>
   </table>
  </td>
 </tr>
 <tr class="source">
  <td class="sourcemargin">
   <a href="../../zhongyuanyinyuntextbyrhyme/
TEXT;
echo $text;
echo $line['rhyme'];
$text = <<<TEXT
">
   
TEXT;
echo $text;
echo $line['rhyme'];
$text = <<<TEXT

   </a>
  </td>
  <td class="sourcelabel">
  
TEXT;
echo $text;
echo $line['homophone'];
$text = <<<TEXT

  </td>
  <td class="sourcelabel">
  
TEXT;
echo $text;
echo $line['reading'];
$text = <<<TEXT

  </td>
  <td class="outersourcetext">
   <table class="sourcetext">
    <tr class="sourcetext">

TEXT;
echo $text;
$oldHomophone = $homophone;
}
$text = <<<TEXT


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
     </td>


TEXT;
echo $text;
$annotation = $line['annotation'];
if($annotation != ""){
$text = <<<TEXT
                         
     <td class="innersourcetext">
     [
TEXT;
echo $text;
echo $annotation;
$text = <<<TEXT
]
     </td>

TEXT;
echo $text;
$oldAnnotation = $annotation;
}
$text = <<<TEXT



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

