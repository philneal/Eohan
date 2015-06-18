<?php
$codepoint=$_GET["codepoint"];

$query = <<<QUERY
SELECT a1.codepoint, a1.glyph, a1.homophone, 
                                  a2.yunjing, 
                                  a3.number, a3.rhyme, a3.finalglyph, a3.tongyong, a3.sectionlabel, 
                                  a4.number, 
                                  b1.id, b1.line, b1.codepoint, b1.glyph, 
                                  b1.rhyme, b1.tone, b1.grade, b1.initial, b1.lmc, 
                                  b2.id, b2.codepoint, b2.glyph, b2.rhyme, b2.tone, 
                                  b2.grade, b2.initial, 
                                  b3.id, b3.rhymelabel, b3.rusheng, b3.fanqie, 
                                  b3.gradekeys1, b3.gradekeys2, b3.gradekeys3, b3.gradekeys4 
                                  FROM (SELECT codepoint, glyph, homophone 
                                  FROM guangyun ) a1, 
                                  (SELECT id, number, final, yunjing 
                                   FROM gyhomophone ) a2, 
                                  (SELECT id, number, tone, rhyme, finalglyph, tongyong, sectionlabel 
                                   FROM gyfinal ) a3, 
                                  (SELECT id, number 
                                   FROM gytone ) a4, 
                                  (SELECT id, line, codepoint, glyph, rhyme, tone, grade, initial, lmc 
                                   FROM yunjing) b1,  
                                  (SELECT id, line, codepoint, glyph, rhyme, tone, grade, initial 
                                   FROM yunjing) b2, 
                                  (SELECT id, rhymelabel, rusheng, fanqie, 
                                   gradekeys1, gradekeys2, gradekeys3, gradekeys4 
                                   FROM yjrhyme ) b3 
                                  WHERE a1.codepoint =  ? 
                                  AND a1.homophone = a2.id 
                                  AND a2.final = a3.id 
                                  AND a3.tone = a4.id 
                                  AND b2.id = a2.yunjing 
                                  AND b2.rhyme = b1.rhyme 
                                  AND b2.rhyme = b3.id 
								  ORDER BY b3.id, b2.id, b1.id
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($codepoint));
$rows = $stmt->fetchAll();
$db=null;

$yunjingLeft = [];
$yunjingRight = [];

foreach($rows as $row){
$codepoint = $row['b1.codepoint'];
$glyph = $row['b1.glyph'];
$initial = $row['b1.initial'];
$grade = $row['b1.grade'];
$tone = $row['b1.tone'];
$lmc = $row['b1.lmc'];
$homophoneId = $row['b1.id'];
$yunjingHomophoneId = $row['b2.id'];
$rhymelabel = $row['b3.rhymelabel'];
$rusheng = $row['b3.rusheng'];
$fanqie = $row['b3.fanqie'];
$gradekeys1 = $row['b3.gradekeys1'];
$gradekeys2 = $row['b3.gradekeys2'];
$gradekeys3 = $row['b3.gradekeys3'];
$gradekeys4 = $row['b3.gradekeys4'];
if($initial > 12){
array_push($yunjingLeft,['codepoint'=>$codepoint,
                            'glyph'=>$glyph,
                            'initial'=>$initial,
                            'grade'=>$grade,
                            'tone'=>$tone,
                            'lmc'=>$lmc,
                            'homophoneid'=>$homophoneId,
                            'yunjinghomophoneid'=>$yunjingHomophoneId,
                            'rhymelabel'=>$rhymelabel,
                            'rusheng'=>$rusheng,
                            'fanqie'=>$fanqie,
                            'gradekeys1'=>$gradekeys1,
                            'gradekeys2'=>$gradekeys2,
                            'gradekeys3'=>$gradekeys3,
                            'gradekeys4'=>$gradekeys4]
							 );
} else {
array_push($yunjingRight,['codepoint'=>$codepoint,
                            'glyph'=>$glyph,
                            'initial'=>$initial,
                            'grade'=>$grade,
                            'tone'=>$tone,
                            'lmc'=>$lmc,
                            'homophoneid'=>$homophoneId,
                            'yunjinghomophoneid'=>$yunjingHomophoneId,
                            'rhymelabel'=>$rhymelabel,
                            'rusheng'=>$rusheng,
                            'fanqie'=>$fanqie,
                            'gradekeys1'=>$gradekeys1,
                            'gradekeys2'=>$gradekeys2,
                            'gradekeys3'=>$gradekeys3,
                            'gradekeys4'=>$gradekeys4]
							 );

}
}

include 'top.php';
$text = <<<TEXT


<link rel="stylesheet" type="text/css" href="../../eohan/css/yunjing.css">
</link>
<h2 class="text">Yunjing</h2>
<h2 class="text">韻鏡</h2>
TEXT;
echo $text;
$text = <<<TEXT
<div class="background">
<table class="doublepage">
 <tr>
    
  <td>
TEXT;
echo $text;
foreach($yunjingLeft as $line){
if($line['initial'] == 23){
if($line['grade'] == 1){
if($line['tone'] == 1){
$text = <<<TEXT
   <h3 class="text">
TEXT;
echo $text;
echo $line['rhymelabel'];
$text = <<<TEXT
</h3>
   <table class="leftpage">
    <tr class="frame">
     <td class="frame">
      <table class="frame">
TEXT;
echo $text;
}
}
}
if($line['initial'] == 23){
$text = <<<TEXT

       <tr class="frame">
        <td class="frame">
         <table class="graderow_
TEXT;
echo $text;
echo $line['grade'];
$text = <<<TEXT
">
          <tr class="frame">

TEXT;
echo $text;
}
if($line['homophoneid'] == $line['yunjinghomophoneid']){
$text = <<<TEXT
    
           <td class="charactercellconcordancematch">
            <table class="initialborder_
TEXT;

} else {
$text = <<<TEXT
    
           <td class="charactercell">
            <table class="initialborder_
TEXT;
}
echo $text;
echo $line['initial'];
$text = <<<TEXT
">
             <tr>

TEXT;
echo $text;
if($line['codepoint'] == 'U+3007'){
$text = <<<TEXT

              <td>
TEXT;
echo $text;
echo $line['glyph'];
$text = <<<TEXT
</td>

TEXT;
echo $text;
} else {
$text = <<<TEXT

              <td><a href="../../eohan/glyph/
TEXT;
echo $text;
echo $line['codepoint'];
$text = <<<TEXT
">
TEXT;
echo $text;
echo $line['glyph'];
$text = <<<TEXT
</a></td>

TEXT;
echo $text;
}
$text = <<<TEXT
             </tr>
            </table>
           </td>
TEXT;
echo $text;
if($line['initial'] == 13){
$text = <<<TEXT
          </tr>
         </table>
        </td>
       </tr>
TEXT;
echo $text;
}
if($line['initial'] == 13){
if($line['grade'] == 4){
if($line['tone'] == 4){
$text = <<<TEXT
      </table>
     </td>
    </tr>
   </table>
TEXT;
echo $text;
}
}
}

}
$text = <<<TEXT
  </td>
  <td>
TEXT;
echo $text;
foreach($yunjingRight as $line){
if($line['initial'] == 12){
if($line['grade'] == 1){
if($line['tone'] == 1){
$text = <<<TEXT
   <h3 class="text">
TEXT;
echo $text;
echo "&nbsp;";
$text = <<<TEXT
</h3>
   <table class="rightpage">
    <tr class="frame">
     <td class="frame">
      <table class="frame">
TEXT;
echo $text;
}
}
}
if($line['initial'] == 12){
$text = <<<TEXT
       <tr class="frame">
        <td class="frame">
         <table class="graderow_
TEXT;
echo $text;
echo $line['grade'];
$text = <<<TEXT
">
          <tr class="frame">

TEXT;
echo $text;
}
if($line['homophoneid'] == $line['yunjinghomophoneid']){
$text = <<<TEXT
    
           <td class="charactercellconcordancematch">
            <table class="initialborder_
TEXT;

} else {
$text = <<<TEXT
    
           <td class="charactercell">
            <table class="initialborder_
TEXT;
}
echo $text;
echo $line['initial'];
$text = <<<TEXT
">
             <tr>

TEXT;
echo $text;
if($line['codepoint'] == 'U+3007'){
$text = <<<TEXT

              <td>
TEXT;
echo $text;
echo $line['glyph'];
$text = <<<TEXT
</td>

TEXT;
echo $text;
} else {
$text = <<<TEXT

              <td><a href="../../eohan/glyph/
TEXT;
echo $text;
echo $line['codepoint'];
$text = <<<TEXT
">
TEXT;
echo $text;
echo $line['glyph'];
$text = <<<TEXT
</a></td>

TEXT;
echo $text;
}
$text = <<<TEXT
             </tr>
            </table>
           </td>
TEXT;
echo $text;
if($line['initial'] == 1){
$text = <<<TEXT
          </tr>
         </table>
        </td>
       </tr>
TEXT;
echo $text;
}
if($line['initial'] == 1){
if($line['grade'] == 4){
if($line['tone'] == 4){
$text = <<<TEXT
      </table>
     </td>
    </tr>
   </table>
TEXT;
echo $text;
}
}
}
}
$text = <<<TEXT
  </td>    
 </tr>
</table>
</div>
<div class="background">

<table class="doublepage">
 <tr>
  <td>
TEXT;
echo $text;
foreach($yunjingLeft as $line){
if($line['initial'] == 23){
if($line['grade'] == 1){
if($line['tone'] == 1){
$text = <<<TEXT
   <table class="leftpage">
    <tr class="frame">
     <td class="frame">
      <table class="frame">
TEXT;
echo $text;
}
}
}
if($line['initial'] == 23){
$text = <<<TEXT
       <tr class="frame">
        <td class="frame">
         <table class="graderow_
TEXT;
echo $text;
echo $line['grade'];
$text = <<<TEXT
">
          <tr class="frame">

TEXT;
echo $text;
}
if($line['homophoneid'] == $line['yunjinghomophoneid']){
$text = <<<TEXT
           <td class="readingcellconcordancematch">
            <table class="initialborder_
TEXT;
} else {
$text = <<<TEXT
           <td class="reading">
            <table class="initialborder_
TEXT;
}
echo $text;
echo $line['initial'];
$text = <<<TEXT
">
             <tr>

TEXT;
echo $text;if($line['lmc'] == ''){
$text = <<<TEXT
              <td class="reading">&#x3007;</td>
TEXT;
echo $text;
} else {
$text = <<<TEXT
              <td class="reading">
TEXT;
echo $text;
echo $line['lmc'];
$text = <<<TEXT
</td>
TEXT;
echo $text;
}
$text = <<<TEXT
           </tr>
            </table>
           </td>
TEXT;
echo $text;
if($line['initial'] == 13){
$text = <<<TEXT
          </tr>
         </table>
        </td>
       </tr>
TEXT;
echo $text;
}
if($line['initial'] == 13){
if($line['grade'] == 4){
if($line['tone'] == 4){
$text = <<<TEXT
      </table>
     </td>
    </tr>
   </table>
TEXT;
echo $text;
}
}
}

}

$text = <<<TEXT
  </td>
 </tr>
</table>
</div>
<div class="background">
<table class="doublepage">
 <tr>
  <td>
TEXT;
echo $text;

foreach($yunjingRight as $line){

if($line['initial'] == 12){
if($line['grade'] == 1){
if($line['tone'] == 1){
$text = <<<TEXT
   <table class="rightpage">
    <tr class="frame">
     <td class="frame">
      <table class="frame">
TEXT;
echo $text;
}
}
}
if($line['initial'] == 12){
$text = <<<TEXT
       <tr class="frame">
        <td class="frame">
         <table class="graderow_
TEXT;
echo $text;
echo $line['grade'];
$text = <<<TEXT
">
          <tr class="frame">
TEXT;
echo $text;
}
if($line['homophoneid'] == $line['yunjinghomophoneid']){
$text = <<<TEXT
           <td class="readingcellconcordancematch">
            <table class="initialborder_
TEXT;
} else {
$text = <<<TEXT
           <td class="readingcell">
            <table class="initialborder_
TEXT;
}
echo $text;
echo $line['initial'];
$text = <<<TEXT
">
             <tr>
TEXT;
echo $text;
if($line['lmc'] == ''){
$text = <<<TEXT

              <td class="reading">&#x3007;</td>

TEXT;
echo $text;
} else {
$text = <<<TEXT

              <td class="reading">
TEXT;
echo $text;
echo $line['lmc'];
$text = <<<TEXT
</td>
TEXT;
echo $text;
}
$text = <<<TEXT
           </tr>
            </table>
           </td>
TEXT;
echo $text;
if($line['initial'] == 1){
$text = <<<TEXT
          </tr>
         </table>
        </td>
       </tr>
TEXT;
echo $text;
}
if($line['initial'] == 1){
if($line['grade'] == 4){
if($line['tone'] == 4){
$text = <<<TEXT
      </table>
     </td>
    </tr>
   </table>
TEXT;
echo $text;
}
}
}

}
$text = <<<TEXT
  </td>
 </tr>
</table>

</div>
TEXT;
echo $text;
include 'bottom.php';
