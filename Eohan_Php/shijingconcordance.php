<?php
$codepoint=$_GET["codepoint"];

$query = <<<QUERY
SELECT b.id, b.codepoint, b.glyph, 
                           b.line, b.isrhyme, b.rhymeset, b.stanza, 
                           b.stanzanumber, b.ode, b.odenumber, 
                           b.odetitle, b.parttitle, b.booktitle, b.booknumber, b.parttitle 
                     FROM (SELECT  a1.id AS id, a1.codepoint AS codepoint, a1.isrhyme AS isrhyme, a1.line AS line 
                     FROM shijing a1, shijingline a2, shijingstanza a3, shijingode a4, shijingbook a5, shijingpart a6 
                     WHERE a1.line = a2.id 
                     AND a2.stanza = a3.id 
                     AND a3.ode = a4.id 
                     AND a4.book = a5.id 
                     AND a5.part = a6.id) a, 
                     (SELECT  b1.id AS id, b1.codepoint AS codepoint, b1.glyph AS glyph, b1.line AS line, 
                     b1.isrhyme AS isrhyme, b2.rhymeset AS rhymeset, 
                     b2.stanza AS stanza, b3.number AS stanzanumber, b3.ode AS ode, b4.number AS odenumber, 
                     b4.title AS odetitle, b5.number AS booknumber, 
                     b5.title AS booktitle, b6.title AS parttitle 
                     FROM shijing b1, shijingline b2, shijingstanza b3, shijingode b4, 
                     shijingbook b5, shijingpart b6 
                     WHERE b1.line = b2.id 
                     AND b2.stanza = b3.id 
                     AND b3.ode = b4.id 
                     AND b4.book = b5.id 
                     AND b5.part = b6.id) b 
                     WHERE a.codepoint = ? 
                     AND a.isrhyme = 1 
                     AND a.line = b.line 
                     ORDER BY a.id, b.id  
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($codepoint));
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

<table class="source">                         


TEXT;
echo $text;
foreach($lines as $line){
$text = <<<TEXT


 <tr>
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
  <td class="outersourcetext">
  
TEXT;
echo $text;
echo $line['odetitle'];
$text = <<<TEXT

  </td> 
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
