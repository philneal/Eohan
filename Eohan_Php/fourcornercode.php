<?php
$codepoint=$_GET["codepoint"];
$query = <<<QUERY
SELECT b.codepoint, b.glyph, b.nwcorner, b.necorner, b.swcorner, b.secorner, b.esecorner, radical.totalstrokes, '0' as direction 
                              FROM fourcornercode a, fourcornercode b, glyph c, glyph d, radical 
                              WHERE 
                              c.codepoint = ? 
                              AND b.codepoint = radical.codepoint 
                              AND a.codepoint = c.codepoint 
                              AND b.codepoint = d.codepoint 
                              AND d.occurrence = 1 
                              AND a.necorner = b.necorner AND a.nwcorner = b.nwcorner 
                              AND a.secorner = b.secorner AND a.swcorner = b.swcorner 
                              UNION ALL 
                              SELECT b.codepoint, b.glyph, b.nwcorner, b.necorner, b.swcorner, b.secorner, b.esecorner, radical.totalstrokes, '1' as direction 
                              FROM fourcornercode a, fourcornercode b, glyph c, glyph d, radical 
                              WHERE 
                              c.codepoint = ? 
                              AND b.codepoint = radical.codepoint 
                              AND a.codepoint = c.codepoint 
                              AND b.codepoint = d.codepoint 
                              AND d.occurrence = 1 
                              AND a.necorner = b.necorner AND a.nwcorner = b.nwcorner AND a.secorner = b.secorner 
                              UNION ALL 
                              SELECT b.codepoint, b.glyph, b.nwcorner, b.necorner, b.swcorner, b.secorner, b.esecorner, radical.totalstrokes, '2' as direction 
                              FROM fourcornercode a, fourcornercode b, glyph c, glyph d, radical 
                              WHERE 
                              c.codepoint = ? 
                              AND b.codepoint = radical.codepoint 
                              AND a.codepoint = c.codepoint 
                              AND b.codepoint = d.codepoint 
                              AND d.occurrence = 1 
                              AND a.necorner = b.necorner AND a.nwcorner = b.nwcorner AND a.swcorner = b.swcorner 
                              UNION ALL 
                              SELECT b.codepoint, b.glyph, b.nwcorner, b.necorner, b.swcorner, b.secorner, b.esecorner, radical.totalstrokes, '3' as direction 
                              FROM fourcornercode a, fourcornercode b, glyph c, glyph d, radical 
                              WHERE 
                              c.codepoint = ? 
                              AND b.codepoint = radical.codepoint 
                              AND a.codepoint = c.codepoint 
                              AND b.codepoint = d.codepoint 
                              AND d.occurrence = 1 
                              AND a.secorner = b.secorner AND a.swcorner = b.swcorner AND a.nwcorner = b.nwcorner 
                              UNION ALL 
                              SELECT b.codepoint, b.glyph, b.nwcorner, b.necorner, b.swcorner, b.secorner, b.esecorner, radical.totalstrokes, '4' as direction 
                              FROM fourcornercode a, fourcornercode b, glyph c, glyph d, radical 
                              WHERE 
                              c.codepoint = ? 
                              AND b.codepoint = radical.codepoint 
                              AND a.codepoint = c.codepoint 
                              AND b.codepoint = d.codepoint 
                              AND d.occurrence = 1 
                              AND a.secorner = b.secorner AND a.swcorner = b.swcorner AND a.necorner = b.necorner 
                              ORDER BY direction, radical.totalstrokes, b.nwcorner, b.necorner, 
                              b.swcorner, b.secorner 
QUERY;

$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($codepoint,$codepoint,$codepoint,$codepoint,$codepoint)); 
$rows = $stmt->fetchAll();
$db=null;

include 'top.php';
$text = <<<TEXT
<h2 class="text">Four Corner Code</h2>
<h3 class="text">
TEXT;
echo $text;
echo $rows[0]['b.nwcorner'];
echo $rows[0]['b.necorner'];
echo $rows[0]['b.swcorner'];
echo $rows[0]['b.secorner'];
$text = <<<TEXT
.
TEXT;
echo $text;
echo $rows[0]['b.esecorner'];
$text = <<<TEXT
</h3>
<h3 class="text">Exact match</h3>
<table class="source">
<tr class="source"><td class="innersourcetext">
TEXT;
echo $text;
foreach($rows as $row){
if($row['direction'] == '0'){
$text = <<<TEXT
<a href="../../glyph/
TEXT;
echo $text;
echo $row['b.codepoint'];
$text = <<<TEXT
">
TEXT;
echo $text;
echo $row['b.glyph'];
$text = <<<TEXT
&nbsp;</a>
TEXT;
echo $text;
}
}
$text = <<<TEXT
</td></tr><tr><td class="innersourcetext">&nbsp;</td></tr>
</table>
<h3 class="text">Near match</h3>
<table class="source">
<tr class="source"><td class="innersourcetext">
TEXT;
echo $text;
foreach($rows as $row){
if($row['direction'] == '1'){
$text = <<<TEXT
<a href="../../eohan/glyph/
TEXT;
echo $text;
echo $row['b.codepoint'];
$text = <<<TEXT
">
TEXT;
echo $text;
echo $row['b.glyph'];
$text = <<<TEXT
&nbsp;</a>
TEXT;
echo $text;
}
}
$text = <<<TEXT
</td></tr><tr><td class="innersourcetext">&nbsp;</td></tr>
<tr class="source"><td class="innersourcetext">
TEXT;
echo $text;
foreach($rows as $row){
if($row['direction'] == '2'){
$text = <<<TEXT
<a href="../../glyph/
TEXT;
echo $text;
echo $row['b.codepoint'];
$text = <<<TEXT
">
TEXT;
echo $text;
echo $row['b.glyph'];
$text = <<<TEXT
&nbsp;</a>
TEXT;
echo $text;
}
}
$text = <<<TEXT
</td></tr><tr><td class="innersourcetext">&nbsp;</td></tr>
<tr class="source"><td class="innersourcetext">
TEXT;
echo $text;
foreach($rows as $row){
if($row['direction'] == '3'){
$text = <<<TEXT
<a href="../../glyph/
TEXT;
echo $text;
echo $row['b.codepoint'];
$text = <<<TEXT
">
TEXT;
echo $text;
echo $row['b.glyph'];
$text = <<<TEXT
&nbsp;</a>
TEXT;
echo $text;
}
}
$text = <<<TEXT
</td></tr><tr><td class="innersourcetext">&nbsp;</td></tr>
<tr class="source"><td class="innersourcetext">
TEXT;
echo $text;
foreach($rows as $row){
if($row['direction'] == '1'){
$text = <<<TEXT
<a href="../../glyph/
TEXT;
echo $text;
echo $row['b.codepoint'];
$text = <<<TEXT
">
TEXT;
echo $text;
echo $row['b.glyph'];
$text = <<<TEXT
&nbsp;</a>
TEXT;
echo $text;
}
}
$text = <<<TEXT
</td></tr><tr><td class="innersourcetext">&nbsp;</td></tr>
</table>
TEXT;
echo $text;

include 'bottom.php';