<?php
$rhyme=$_GET["rhyme"];

$query = <<<QUERY
SELECT * 
                    FROM (SELECT zhongyuanyinyun.codepoint, zhongyuanyinyun.glyph, 
                    zhongyuanyinyun.annotation, earlymandarin.reading, 
                    zyhomophone.id, zyhomophone.number, zyfinal.rhyme, zyfinal.label, 
                    zyrhyme.label AS label1 
                    FROM zhongyuanyinyun, earlymandarin, zyhomophone, zyfinal, zyrhyme 
                    WHERE zhongyuanyinyun.homophone = earlymandarin.id 
                    AND zhongyuanyinyun.homophone = zyhomophone.id 
                    AND zyhomophone.final = zyfinal.id 
                    AND zyrhyme.id = zyfinal.rhyme 
                    AND zyrhyme.number = ? ) 
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($rhyme));
$rows = $stmt->fetchAll();
$db=null;
$zhongyuanYinyun = [];
foreach($rows as $row){
$codepoint = $row['codepoint'];
$glyph = $row['glyph'];
$reading = $row['reading'];
$annotation = $row['annotation'];
$finallabel = $row['label'];
array_push($zhongyuanYinyun,['codepoint'=>$codepoint,
                            'glyph'=>$glyph,
                            'reading'=>$reading,
                            'annotation'=>$annotation,
                            'label'=>$finallabel]
							 );
}

include 'top.php';

$text = <<<TEXT
<h2 class="text">Zhongyuan Yinyun</h2>
<h2 class="text">中原音韻</h2>
<h3 class="text">
TEXT;
echo $text;
echo $zhongyuanYinyun[0]['label'];
$text = <<<TEXT
</h3>

<table class="source">
 <tr class="source">
  <td class="sourcemargin">
  </td>
  <td class="outersourcetext">
   <table class="sourcetext">
    <tr class="sourcetext">


TEXT;
echo $text;
$oldLabel = "£££";
$oldReading = "£££";
$oldLineAnnotation = "";
foreach($zhongyuanYinyun as $line){
$text = <<<TEXT
                         


TEXT;
echo $text;
$label = $line['label'];
if($label != $oldLabel){
$text = <<<TEXT

    </tr>
   </table>
  </td>
 </tr>
 <tr class="source">
  <td class="sourcemargin">
  </td>
  <td class="outersourcetext">
   <table class="sourcetext">
    <tr class="sourcetext">
      <td class="innersourcetext">
      <h3>
      
TEXT;
echo $text;
echo $label;
$oldLabel = $label;

$text = <<<TEXT

      </h3>
     </td>

TEXT;
echo $text;
}
$reading = $line['reading'];
if($reading != $oldReading){
$text = <<<TEXT
                          
    </tr>
   </table>
  </td>
 </tr>
 <tr class="source">
  <td class="sourcemargin">
  
TEXT;
echo $text;
echo $reading;
$oldReading = $reading;
$text = <<<TEXT

  </td>
  <td class="outersourcetext">
   <table class="sourcetext">
    <tr class="sourcetext">

TEXT;
echo $text;
}
$text = <<<TEXT


     <a id=
TEXT;
echo $text;
echo $line['codepoint'];
$text = <<<TEXT
>
     </a>
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
$lineAnnotation = $line['annotation'];
if($lineAnnotation != ""){
$text = <<<TEXT
                         
     <td class="innersourcetext">
     [
TEXT;
echo $text;
echo $lineAnnotation;
$oldLineAnnotation = $lineAnnotation;
$text = <<<TEXT
]
     </td>

TEXT;
echo $text;
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

