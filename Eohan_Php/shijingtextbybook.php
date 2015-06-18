<?php
$book=$_GET["book"];

$query = <<<QUERY
SELECT 
                    shijing.id, shijing.codepoint, shijing.glyph, 
                    shijing.line, shijing.isrhyme, 
                    shijingline.rhymeset, shijingline.stanza, 
                    shijingstanza.number, shijingstanza.ode, 
                    shijingode.number, 
                    shijingode.title, shijingbook.title, shijingbook.number, shijingpart.title 
                    FROM shijing, shijingline, shijingstanza, shijingode, shijingbook, shijingpart 
                    WHERE shijingbook.number = ? 
                    AND shijing.line = shijingline.id 
                    AND shijingline.stanza = shijingstanza.id 
                    AND shijingstanza.ode = shijingode.id 
                    AND shijingode.book = shijingbook.id 
                    AND shijingbook.part = shijingpart.id 
                    ORDER BY shijing.id 
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($book));
$rows = $stmt->fetchAll();
$db=null;
$shijing = [];
$oldShijingLine = $rows[0][3];
$line = ['id'=>$rows[0][0],
		 'codepoints'=>[$rows[0][1]],
		 'glyphs'=>[$rows[0][2]],
		 'shijingline'=>$rows[0][3],
		 'isrhyme'=>$rows[0][4],
		 'rhymeset'=>$rows[0][5],
		 'stanza'=>$rows[0][6],
		 'stanzanumber'=>$rows[0][7],
		 'ode'=>$rows[0][8],
		 'odenumber'=>$rows[0][9],
		 'odetitle'=>$rows[0][10],
		 'booktitle'=>$rows[0][11],
		 'booknumber'=>$rows[0][12],
		 'parttitle'=>$rows[0][13],
		 'rhymes'=>[],
		 'rhymesets'=>[]];
$lines = [];

$rows = array_slice($rows,1);
foreach($rows as $row){
	$shijingId = $row[0];
	$codepoint = $row[1];
	$glyph = $row[2];
	$shijingLine = $row[3];
	$isRhyme = $row[4];
	$rhymeset = $row[5];
	$stanza = $row[6];
	$stanzanumber = $row[7];
	$ode = $row[8];
	$odenumber = $row[9];
	$odetitle = $row[10];
	$booktitle = $row[11];
	$booknumber = $row[12];
	$parttitle = $row[13];

	if($oldShijingLine != $shijingLine){
	$oldShijingLine = $shijingLine;
	array_push($lines,$line);
	$line = ['id'=>$shijingId,
			 'codepoints'=>[$codepoint],
			 'glyphs'=>[$glyph],
			 'shijingline'=>$shijingLine,
			 'isrhyme'=>$isRhyme,
			 'rhymeset'=>$rhymeset,
			 'stanza'=>$stanza,
			 'stanzanumber'=>$stanzanumber,
			 'ode'=>$ode,
			 'odenumber'=>$odenumber,
			 'odetitle'=>$odetitle,
			 'booktitle'=>$booktitle,
			 'booknumber'=>$booknumber,
			 'parttitle'=>$parttitle,
			 'rhymes'=>[],
			 'rhymesets'=>[]];
	if($isRhyme == 1){
	array_push($line['rhymes'],$glyph);
	array_push($line['rhymesets'],$rhymeset);
	}
	}	else {
	array_push($line['codepoints'],$codepoint);
	array_push($line['glyphs'],$glyph);
	}
	if($isRhyme==1 and !in_array($glyph,$line['rhymes'])){
	array_push($line['rhymes'],$glyph);
	array_push($line['rhymesets'],$rhymeset);
	}
}

array_push($lines,$line);

include 'top.php';
$text = <<<TEXT
<h2 class="text">Shijing</h2>
<h2 class="text">詩經</h2>
<h3 class="text">
TEXT;
echo $text;
echo $lines[0]['parttitle'];
$text = <<<TEXT
</h3>
<h3 class="text">
TEXT;
echo $text;
echo $lines[0]['booktitle'];
$text = <<<TEXT
</h3>

<table class="source">                         
TEXT;
echo $text;
$oldStanzaNumber = 0;

foreach($lines as $line){
$text = <<<TEXT


 <tr>


TEXT;
echo $text;
if($oldStanzaNumber != $line['stanzanumber']){
$text = <<<TEXT

  <td class="sourcemargin">
  
TEXT;
echo $text;
echo $line['odenumber'];
$text = <<<TEXT
.
TEXT;
echo $text;
echo $line['stanzanumber'];
$text = <<<TEXT

  </td>

TEXT;
echo $text;
if($line['stanzanumber'] == "1"){
$text = <<<TEXT

  <td class="outersourcetext">
  
TEXT;
echo $text;
echo $line['odetitle'];
$text = <<<TEXT

  </td>

TEXT;
echo $text;
} else {
$text = <<<TEXT

  <td class="outersourcetext">
  </td>

TEXT;
echo $text;
}
$oldStanzaNumber = $line['stanzanumber'];
$text = <<<TEXT


TEXT;
echo $text;
} else {
$text = <<<TEXT

  <td class="sourcemargin">
  </td>
  <td class="outersourcetext">
  </td>

TEXT;
echo $text;
}
$text = <<<TEXT

 
  <td class="outersourcetext">

TEXT;
echo $text;
$ctr = 0;
foreach($line['glyphs'] as $glyph){
$text = <<<TEXT

  <a href="../glyph/
TEXT;
echo $text;
echo $line['codepoints'][$ctr];
$text = <<<TEXT
"> 
  
TEXT;
echo $text;
echo $glyph;
$text = <<<TEXT

  </a>

TEXT;
echo $text;
$ctr++;
}
$text = <<<TEXT

  </td>

  <td class="sourcelabel">

TEXT;
echo $text;
foreach($line['rhymes'] as $rhyme){
$text = <<<TEXT

  
TEXT;
echo $text;
echo $rhyme;
$text = <<<TEXT


TEXT;
echo $text;
}
$text = <<<TEXT

  </td>
 
  <td class="sourcelabel">

TEXT;
echo $text;
foreach($line['rhymesets'] as $rhymeset){
$text = <<<TEXT

  
TEXT;
echo $text;
echo $rhymeset;
$text = <<<TEXT


TEXT;
echo $text;
}
$text = <<<TEXT

  </td>

 </tr>

TEXT;
echo $text;
}
$text = <<<TEXT

 
</table>                                     



TEXT;
echo $text;
include 'bottom.php';

