<?php
$rhyme=$_GET["rhyme"];

$query = <<<QUERY
SELECT a.id, a.codepoint, a.glyph, a.initial, a.phonation, a.articulation, 
                    a.grade, a.tone, a.line, a.lmc, a.rhyme, a.guangyun, 
                    b.rhymelabel, b.rusheng, b.fanqie, b.gradekeys1, b.gradekeys2, b.gradekeys3, b.gradekeys4 
                    FROM yunjing a, 
                    yjrhyme b 
                    WHERE rhyme = ? 
                    AND a.rhyme = b.id 
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($rhyme));
$rows = $stmt->fetchAll();
$db=null;
$yunjingLeft = [];
$yunjingRight = [];

foreach($rows as $row){
$codepoint = $row['codepoint'];
$glyph = $row['glyph'];
$initial = $row['initial'];
$grade = $row['grade'];
$lmc = $row['lmc'];
$rhymelabel = $row['rhymelabel'];
$rusheng = $row['rusheng'];
$fanqie = $row['fanqie'];
$gradekeys1 = $row['gradekeys1'];
$gradekeys2 = $row['gradekeys2'];
$gradekeys3 = $row['gradekeys3'];
$gradekeys4 = $row['gradekeys4'];
if($initial > 12){
array_push($yunjingLeft,['codepoint'=>$codepoint,
                            'glyph'=>$glyph,
                            'initial'=>$initial,
                            'grade'=>$grade,
                            'lmc'=>$lmc,
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
                            'lmc'=>$lmc,
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
<h3 class="text">
TEXT;
echo $text;
echo $yunjingLeft[0]['rhymelabel'];
$text = <<<TEXT
</h3>
<h3 class="text">
TEXT;
echo $text;
echo $yunjingLeft[0]['rusheng'];
$text = <<<TEXT
&nbsp;
TEXT;
echo $text;
echo $yunjingLeft[0]['fanqie'];
$text = <<<TEXT

&nbsp;
TEXT;
echo $text;
echo $yunjingLeft[0]['gradekeys1'];
$text = <<<TEXT
&nbsp;
&nbsp;
TEXT;
echo $text;
echo $yunjingLeft[0]['gradekeys2'];
$text = <<<TEXT
&nbsp;
&nbsp;
TEXT;
echo $text;
echo $yunjingLeft[0]['gradekeys3'];
$text = <<<TEXT
&nbsp;
&nbsp;
TEXT;
echo $text;
echo $yunjingLeft[0]['gradekeys4'];
$text = <<<TEXT
</h3>

<div class="background">
<table class="doublepage">
 <tr>
    
  <td>
   <table class="leftpage">
    <tr class="frame">
     <td class="frame">
    
      <table class="frame">

       
TEXT;
echo $text;
$text = <<<TEXT



TEXT;
echo $text;
foreach($yunjingLeft as $line){
$text = <<<TEXT


TEXT;
echo $text;
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
$text = <<<TEXT
    
           <td class="charactercell">
            <table class="initialborder_
TEXT;
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
$text = <<<TEXT



TEXT;
echo $text;
}
$text = <<<TEXT

   
      </table>
    
     </td>
    </tr>
   </table>
  </td>
  <td>
   <table class="rightpage">
    <tr class="frame">
     <td class="frame">    
      <table class="frame">


TEXT;

echo $text;
foreach($yunjingRight as $line){
$text = <<<TEXT



TEXT;
echo $text;
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
$text = <<<TEXT

    
           <td class="charactercell">
            <table class="initialborder_
TEXT;
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
$text = <<<TEXT



TEXT;
echo $text;
}

$text = <<<TEXT

    
      </table>
    
     </td>
    </tr>
   </table>
    
  </td>
 </tr>
</table>
    
</div>
    
<div class="background">

<table class="doublepage">
 <tr>
  <td>
    
   <table class="leftpage">
    <tr class="frame">
     <td class="frame">
    
      <table class="frame">


TEXT;
echo $text;
foreach($yunjingLeft as $line){
$text = <<<TEXT
    

TEXT;
echo $text;
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
$text = <<<TEXT
    
           <td class="readingcell">
            <table class="initialborder_
TEXT;
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
if($line['initial'] == 13){
$text = <<<TEXT

          </tr>
         </table>
        </td>
       </tr>

TEXT;
echo $text;
}
$text = <<<TEXT



TEXT;
echo $text;
}
$text = <<<TEXT
    
      </table>
    
     </td>
    </tr>
   </table>
  </td>

    
  </td>
 </tr>
</table>
    
</div>
    
<div class="background">

<table class="doublepage">
 <tr>
  <td>
    
   <table class="rightpage">
    <tr class="frame">
     <td class="frame">
    
      <table class="frame">


TEXT;
echo $text;
foreach($yunjingRight as $line){
$text = <<<TEXT
    

TEXT;
echo $text;
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
$text = <<<TEXT
    
           <td class="readingcell">
            <table class="initialborder_
TEXT;
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
$text = <<<TEXT



TEXT;
echo $text;
}echo $text;

$text = <<<TEXT
    
      </table>
    
     </td>
    </tr>
   </table>
  </td>
    
  </td>
 </tr>
</table>
    
</div>


TEXT;
echo $text;
include 'bottom.php';
