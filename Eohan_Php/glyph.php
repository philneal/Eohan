<?php
include 'top.php';
$codepoint=$_GET["codepoint"];

$query = <<<QUERY
                     SELECT 'glyph' AS field, glyph.glyph 
                     FROM glyph  
                     WHERE glyph.codepoint = ?  
                     UNION ALL  
                     SELECT 'codepoint' AS field, glyph.codepoint 
                     FROM glyph  
                     WHERE glyph.codepoint = ?  
                     UNION ALL  
                     SELECT 'mandarin' AS field, pinyin FROM mandarin  
                     WHERE mandarin.codepoint = ?  
                     UNION ALL  
                     SELECT 'cantonese' AS field, reading FROM cantonese  
                     WHERE cantonese.codepoint = ?  
                     UNION ALL  
                     SELECT 'japaneseon' AS field, reading FROM japaneseon  
                     WHERE japaneseon.codepoint = ?  
                     UNION ALL  
                     SELECT 'korean' AS field, reading FROM korean  
                     WHERE korean.codepoint = ?  
                     UNION ALL  
                     SELECT 'vietnamese' AS field, reading FROM vietnamese  
                     WHERE vietnamese.codepoint = ?  
                     UNION ALL  
                     SELECT 'earlymandarin' AS field, reading FROM zhongyuanyinyun, earlymandarin  
                     WHERE zhongyuanyinyun.homophone = earlymandarin.id  
                     AND zhongyuanyinyun.codepoint = ?  
                     UNION ALL  
                     SELECT 'lmc' AS field, lmc FROM  
                     (SELECT * FROM guangyun, gyhomophone, yunjing  
                     WHERE guangyun.homophone = gyhomophone.id  
                     AND gyhomophone.yunjing = yunjing.id 
                     AND guangyun.codepoint = ?)  
                     UNION ALL  
                     SELECT 'mcb' AS field, mcb FROM  
                     (SELECT * FROM guangyun, gyhomophone   
                     WHERE guangyun.homophone = gyhomophone.id  
                     AND guangyun.codepoint = ?)  
                     UNION ALL  
                     SELECT 'emc' AS field, emc FROM  
                     (SELECT * FROM guangyun, gyhomophone   
                     WHERE guangyun.homophone = gyhomophone.id  
                     AND guangyun.codepoint = ?)  
                     UNION ALL  
                     SELECT  'mck' AS field, mck FROM  
                     (SELECT * FROM guangyun, gyhomophone   
                     WHERE guangyun.homophone = gyhomophone.id  
                     AND guangyun.codepoint = ?)  
                     UNION ALL  
                     SELECT  'baxter' AS field, baxter FROM gsr  
                     WHERE gsr.codepoint = ?  
                     UNION ALL  
                     SELECT  'baxterfinal' AS field, baxterfinal FROM gsr  
                     WHERE gsr.codepoint = ?  
                     UNION ALL  
                     SELECT  'pulleyblank' AS field, pulleyblank FROM gsr  
                     WHERE gsr.codepoint = ?  
                     UNION ALL  
                     SELECT  'pulleyblankfinal' AS field, pulleyblankfinal FROM gsr  
                     WHERE gsr.codepoint = ?  
                     UNION ALL  
                     SELECT  'karlgren' AS field, karlgren FROM gsr  
                     WHERE gsr.codepoint = ?  
                     UNION ALL  
                     SELECT  'karlgrenfinal' AS field, karlgrenfinal FROM gsr  
                     WHERE gsr.codepoint = ?  
                     UNION ALL  
                     SELECT  'radicalnumber' AS field, radicalnumber FROM radical  
                     WHERE radical.codepoint = ?  
                     UNION ALL  
                     SELECT  'strokecount' AS field, strokecount FROM radical  
                     WHERE radical.codepoint = ?  
                     UNION ALL  
                     SELECT  'nwcorner' AS field, nwcorner FROM fourcornercode  
                     WHERE fourcornercode.codepoint = ?  
                     UNION ALL  
                     SELECT  'necorner' AS field, necorner FROM fourcornercode  
                     WHERE fourcornercode.codepoint = ?  
                     UNION ALL  
                     SELECT  'swcorner' AS field, swcorner FROM fourcornercode  
                     WHERE fourcornercode.codepoint = ?  
                     UNION ALL  
                     SELECT  'secorner' AS field, secorner FROM fourcornercode  
                     WHERE fourcornercode.codepoint = ?  
                     UNION ALL  
                     SELECT  'esecorner' AS field, esecorner FROM fourcornercode  
                     WHERE fourcornercode.codepoint = ?  
                     UNION ALL  
                     SELECT  'karlgrenseries' AS field, series FROM karlgren  
                     WHERE codepoint = ?  
                     UNION ALL  
                     SELECT  'wieger' AS field, phonetic FROM wieger  
                     WHERE wieger.codepoint = ?  
                     UNION ALL  
                     SELECT 'guangyun' AS field, COUNT (*) FROM guangyun 
                     WHERE  codepoint = ? 
                     UNION ALL 
                     SELECT 'yunjing' AS field, COUNT (*) FROM yunjing 
                     WHERE  codepoint = ? 
                     UNION ALL 
                     SELECT 'shijing' AS field, COUNT (*) FROM shijing  
                     WHERE  codepoint = ? 
                     UNION ALL 
                     SELECT  'gsr' AS field, COUNT (*) FROM gsr  
                     WHERE  codepoint = ? 
                     UNION ALL 
                     SELECT  'zhongyuanyinyun' AS field, COUNT (*) FROM zhongyuanyinyun  
                     WHERE codepoint = ? 
QUERY;
$db = new PDO('sqlite:database/cp.db');
$stmt = $db->prepare($query);
$stmt->execute(array($codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint,$codepoint));
$rows = $stmt->fetchAll();
$db=null;

$glyphDict = ['glyph' => [], 
                   'codepoint' => [],
                   'mandarin' => [],
                   'cantonese' => [],
                   'japaneseon' => [],
                   'korean' => [],
                   'vietnamese' => [],
                   'earlymandarin' => [],
                   'lmc' => [],
                   'emc' => [],
                   'mcb' => [],
                   'mck' => [],
                   'baxter' => [],
                   'baxterfinal' => [],
                   'pulleyblank' => [],
                   'pulleyblankfinal' => [],
                   'karlgren' => [],
                   'karlgrenfinal' => [],
                   'radicalnumber' => [],
                   'strokecount' => [],
                   'nwcorner' => [],
                   'necorner' => [],
                   'swcorner' => [],
                   'secorner' => [],
                   'esecorner' => [],
                   'karlgrenseries' => [],
                   'wieger' => [],
                   'guangyun' => [],
                   'yunjing' => [],
                   'shijing' => [],
                   'gsr' => [],
                   'zhongyuanyinyun' => []];
				   
foreach($rows as $row){
$key = $row[0];
$value = $row[1];
array_push($glyphDict[$key],$value);
}

$text = <<<TEXT
<h1 id="glyphheader" align=center>                
TEXT;
echo $text;
$glyph = $glyphDict['glyph'][0];
echo $glyph;
$text = <<<TEXT


</h1>

<table id="data" align=center>
 <tr>
  <td valign=top>



   <table id="dialects" class="datacolumn">       
    <tr>
     <th class="dataheader">                      
     Dialects
     </th>
    </tr>
    <tr>
     <td class="dataset" valign=top>              
     Mandarin
     </td>                                        
     <td class="datavalues">                      
      <table>                                     
TEXT;
echo $text;
$mandarin = $glyphDict['mandarin'];
foreach ($mandarin as $reading){
$text = <<<TEXT

       <tr>
        <td>
         <a href = "../../eohan/mandarin/
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT

">
         
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT


         </a>
        </td>
       </tr>
TEXT;
echo $text;
}
$text = <<<TEXT

      </table>
     </td>
    </tr>
    
    <tr>
     <td class="dataset" valign=top>
     Cantonese
     </td>
     <td class="datavalues">
      <table>
TEXT;
echo $text;
$cantonese = $glyphDict['cantonese'];
foreach ($cantonese as $reading){
$text = <<<TEXT

       <tr>
        <td>
         <a href = "../../eohan/cantonese/
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT

">
         
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT


         </a>
        </td>
       </tr>
TEXT;
echo $text;
}
$text = <<<TEXT

      </table>
     </td>
    </tr>
    <tr>
     <td>
     </td>
     <td>
     </td>
    </tr>
   </table>
  </td>

   <td valign=top>
    <table id="sinoxenic" class="datacolumn">     
     <tr>
      <th class="dataheader" colspan=2>           
      Sinoxenic
      </th>
     </tr>                                         
     <tr>
      <td class="dataset" valign=top>             
      Japanese
      </td>
      <td class="datavalues">                     
       <table>                                     
TEXT;
echo $text;
$japaneseon = $glyphDict['japaneseon'];
foreach ($japaneseon as $reading){
$text = <<<TEXT

        <tr>
         <td>
          <a href = "../../eohan/japanese/
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT

">
          
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT


          </a>
         </td>
        </tr>
TEXT;
echo $text;
}
$text = <<<TEXT

       </table>
      </td>
     </tr>
     <tr>
      <td class="dataset" valign=top>
      Korean
      </td>
      <td class="datavalues">
       <table>
TEXT;
echo $text;
$korean = $glyphDict['korean'];
foreach($korean as $reading){
$text = <<<TEXT

        <tr>
         <td>
          <a href = "../../eohan/korean/
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT

">
          
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT


          </a>
         </td>
        </tr>
TEXT;
echo $text;
}
$text = <<<TEXT

       </table>
      </td>
     </tr>
     <tr>
      <td valign=top>
      Vietnamese
      </td>
      <td class="datavalues">
       <table>
TEXT;
echo $text;
$vietnamese  = $glyphDict['vietnamese'];
foreach( $vietnamese as $reading){
$text = <<<TEXT

        <tr>
         <td>
          <a href = "../../eohan/vietnamese/
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT

">
          
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT


          </a>
         </td>
        </tr>
TEXT;
echo $text;
}
$text = <<<TEXT

       </table>
      </td>
     </tr>
    </table>
   </td>



   <td valign=top>
    <table id="graphical" class="datacolumn">     
     <tr>
      <th class="dataheader" colspan=2>           
      Graphical
      </th>
     </tr>                                        
     <tr>
      <td class="dataset" valign=top>             
      Radical
      </td>                                       
      <td>
       <a href="../../eohan/radical/
TEXT;
echo $text;
$radicalnumber = $glyphDict['radicalnumber'];
echo $radicalnumber[0];
$text = <<<TEXT

">
       
TEXT;
echo $text;
echo $radicalnumber[0];
$text = <<<TEXT

.
TEXT;
echo $text;
$strokecount = $glyphDict['strokecount'];
echo $strokecount[0];
$text = <<<TEXT


       </a>
      </td>
     </tr>
     <tr>
      <td class="dataset" valign=top>             
      Four Corner Code
      </td>                                       
      <td>
       <a href="../../eohan/fourcornercode/
TEXT;
echo $text;
echo $codepoint;
$text = <<<TEXT

">
       
TEXT;
echo $text;
$nwcorner = $glyphDict['nwcorner'];
if (count($nwcorner) > 0){
echo $nwcorner[0];
} else {
echo "&nbsp;";
}
$text = <<<TEXT


TEXT;
echo $text;
if (count($nwcorner) > 0){
$necorner  = $glyphDict['necorner'];
echo $necorner[0];
} else {
echo "&nbsp;";
}
$text = <<<TEXT


TEXT;
echo $text;
if (count($nwcorner) > 0){
$swcorner  = $glyphDict['swcorner'];
echo $swcorner[0];
} else {
echo "&nbsp;";
}
$text = <<<TEXT


TEXT;
echo $text;
if (count($nwcorner) > 0){
$secorner = $glyphDict['secorner'];
echo $secorner[0];
} else {
echo "&nbsp;";
}
$text = <<<TEXT

.
TEXT;
echo $text;
if (count($nwcorner) > 0){
$esecorner = $glyphDict['esecorner'];
echo $esecorner[0];
} else {
echo "&nbsp;";
}
$text = <<<TEXT


       </a>
      </td>
     </tr>
     <tr>
      <td class="dataset" valign=top>             
      Karlgren
      </td>           
      <td class="datavalues">                     
       <table>                                    
TEXT;
echo $text;
$karlgrenseries = $glyphDict['karlgrenseries'];
foreach ($karlgrenseries as $series){
$text = <<<TEXT

        <tr>
         <td>
          <a href="../../eohan/karlgren/
TEXT;
echo $text;
echo $series;
$text = <<<TEXT

">
          
TEXT;
echo $text;
echo $series;
$text = <<<TEXT


          </a>
         </td>
        </tr>
TEXT;
echo $text;
}
$text = <<<TEXT

       </table>
      </td>
     </tr>
     <tr>
      <td class="dataset" valign=top>             
      Wieger
      </td>                                       
      <td class="datavalues">                     
       <table>                                    
TEXT;
echo $text;
$wieger = $glyphDict['wieger'];
foreach($wieger as $series){
$text = <<<TEXT

        <tr>
         <td>
          <a href="../../eohan/wieger/
TEXT;
echo $text;
echo $series;
$text = <<<TEXT

">
          
TEXT;
echo $text;
echo $series;
$text = <<<TEXT


          </a>
         </td>
        </tr>
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

 <table>
  <tr>
    <td>&nbsp;
    </td>
  </tr>
 </table>


 <table id="reconstruction" align=center>
  <tr>


   <td valign=top>
    <table id="concordances" class="datacolumn">       
     <tr>
      <th class="dataheader" colspan=2>           
      Sources
      </th>
     </tr>                             
     <tr>
      <td class="dataset">                        
      </td>
      <td class="datavalues">
      </td>
     </tr>                                        
     <tr>
      <td>
      Zhongyuan Yinyun
      </td>
TEXT;
echo $text;
$zhongyuanyinyun  = $glyphDict['zhongyuanyinyun'];
if ($zhongyuanyinyun != 0){
$text = <<<TEXT

      <td>
       <a href="../../eohan/zhongyuanyinyunconcordance/
TEXT;
echo $text;
echo $codepoint;
$text = <<<TEXT

">
       Zhongyuan Yinyun
       </a>
      </td>
TEXT;
echo $text;
} else {
$text = <<<TEXT

      <td>
      </td>
TEXT;
echo $text;
}
$text = <<<TEXT

     </tr>
     <tr>
     </tr>
     <tr>
      <td>
      Yunjing
      </td>
TEXT;
echo $text;
$yunjing = $glyphDict['yunjing'];
if ($yunjing[0] != 0){
$text = <<<TEXT

      <td>
       <a href="../../eohan/yunjingconcordance/
TEXT;
echo $text;
echo $codepoint;
$text = <<<TEXT

">
       Yunjing
       </a>
      </td>
TEXT;
echo $text;
} else {
$text = <<<TEXT

      <td>
      </td>
TEXT;
echo $text;
}
$text = <<<TEXT

     </tr>
     <tr>
      <td>
      Guangyun
      </td>
TEXT;
echo $text;
$guangyun = $glyphDict['guangyun'];
if ($guangyun != 0){
$text = <<<TEXT

      <td>
       <a href="../../eohan/guangyunconcordance/
TEXT;
echo $text;
echo $codepoint;
$text = <<<TEXT

">
       Guangyun
       </a>
      </td>
TEXT;
echo $text;
} else {
$text = <<<TEXT

      <td>
      </td>
TEXT;
echo $text;
}
$text = <<<TEXT

     </tr>
     <tr>
      <td>
      Shijing
      </td>
TEXT;
echo $text;
$shijing = $glyphDict['shijing'];
if ($shijing != 0){
$text = <<<TEXT

      <td>
       <a href="../../eohan/shijingconcordance/
TEXT;
echo $text;
echo $codepoint;
$text = <<<TEXT

">
       Shijing
       </a>
      </td>
TEXT;
echo $text;
} else {
$text = <<<TEXT

      <td>
      </td>
TEXT;
echo $text;
}
$text = <<<TEXT

     </tr>
     <tr>
      <td>
      GSR
      </td>
TEXT;
echo $text;
$gsr = $glyphDict['gsr'];
if ($gsr != 0){
$text = <<<TEXT

      <td>
       <a href="../../eohan/gsrconcordance/
TEXT;
echo $text;
echo $codepoint;
$text = <<<TEXT

">
       GSR
       </a>
      </td>
TEXT;
echo $text;
} else {
$text = <<<TEXT

      <td>
      </td>
TEXT;
echo $text;
}
$text = <<<TEXT

     </tr>
    </table>
   </td>


   <td valign=top>
    <table id="pulleyblank" class="datacolumn">   
     <tr>
      <th class="dataheader" colspan=2>           
      Pulleyblank system
      </th>
     </tr>         
     <tr>
      <td class="dataset" valign=top>             
      Early Mandarin
      </td>           
      <td class="datavalues">
       <table>                                    
TEXT;
echo $text;
$earlymandarin = $glyphDict['earlymandarin'];
foreach ($earlymandarin as $reading){
$text = <<<TEXT

        <tr>
         <td>
          <a href="../../eohan/em/
TEXT;
echo $text;
echo $reading;

$text = <<<TEXT

">
          
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT


          </a>
         </td>
        </tr>
TEXT;
echo $text;
}
$text = <<<TEXT

       </table>
      </td>
     </tr>
     <tr>
      <td class="dataset" valign=top>             
      Late Middle Chinese
      </td>                        
      <td class="datavalues">                     
TEXT;
echo $text;
$lmc  = $glyphDict['lmc'];
foreach($lmc as $reading){
$text = <<<TEXT

       <table>
        <tr>
         <td>
          <a href="../../eohan/lmc/
TEXT;
echo $text;
echo $reading;

$text = <<<TEXT

">
          
TEXT;
echo $text;
echo $reading;

$text = <<<TEXT


          </a>
         </td>
        </tr>
TEXT;
echo $text;
}
$text = <<<TEXT

       </table>
      </td>
     </tr>
     <tr>
      <td class="dataset" valign=top>             
      Early Middle Chinese
      </td>     
      <td class="datavalues">                     
       <table>                                    
TEXT;
echo $text;
$emc = $glyphDict['emc'];
foreach ($emc as $reading){
$text = <<<TEXT

        <tr>
         <td>
          <a href="../../eohan/emc/
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT

">
          
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT


          </a>
         </td>
        </tr>
TEXT;
echo $text;
}
$text = <<<TEXT

       </table>
      </td>
     </tr>
     <tr>
      <td class="dataset" valign=top>             
      Old Chinese
      </td>                                       
      <td class="datavalues">                     
       <table>                                    
TEXT;
echo $text;
$pulleyblank = $glyphDict['pulleyblank'];
foreach ($pulleyblank as $key => $value){
$text = <<<TEXT

        <tr>
         <td>
          <a href="../../eohan/ocp/
TEXT;
echo $text;
$pulleyblankfinal  = $glyphDict['pulleyblankfinal'];
echo $pulleyblankfinal[$key];
$text = <<<TEXT

"
          </a>
          
TEXT;
echo $text;
echo $pulleyblank[$key];

$text = <<<TEXT


         </td>
        </tr>
TEXT;
echo $text;
}
$text = <<<TEXT

       </table>
      </td>
     </tr>
    </table>
   </td>

   <td valign=top>
    <table id="baxter" class="datacolumn">        
     <tr>
      <th class="dataheader" colspan=2>
      Baxter system
      </th>
     </tr>                                        
     <tr>
      <td class="dataset">
      </td>
      <td class="datavalues">
      </td>
     </tr>                                        
     <tr>
      <td class="dataset" valign=top>
      Middle Chinese
      </td>                                       
      <td class="datavalues">
       <table>                                   
TEXT;
echo $text;
$mcb = $glyphDict['mcb'];
foreach ($mcb as $reading){
$text = <<<TEXT

        <tr>
         <td>
          <a href="../../eohan/mcb/
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT

">
          
TEXT;
echo $text;
echo $reading;
$text = <<<TEXT


          </a>
         </td>
        </tr>
TEXT;
echo $text;
}
$text = <<<TEXT

       </table>
      </td>
     </tr>
     <tr>
      <td class="dataset">                        
      </td>
      <td>
      </td>
     </tr>                
     <tr>
      <td class="dataset" valign=top>             
      Old Chinese
      </td>                          
      <td class="datavalues">
       <table>
TEXT;
echo $text;
$baxter = $glyphDict['baxter'];
foreach ($baxter as $key => $value){
$text = <<<TEXT

        <tr>
         <td>
          <a href="../../eohan/ocb/
TEXT;
echo $text;
$baxterfinal = $glyphDict['baxterfinal'];
echo $baxterfinal[$key];
$text = <<<TEXT

"
          </a>
          
TEXT;
echo $text;
echo $baxter[$key];
$text = <<<TEXT


         </td>
        </tr>
TEXT;
echo $text;
}
$text = <<<TEXT

       </table>
      </td>
     </tr>
    </table>
   </td>

      

   <td valign=top>
    <table id="baxter" class="datacolumn">        
     <tr>
      <th class="dataheader" colspan=2>
      Karlgren system
      </th>
     </tr>                                        
     <tr>
      <td class="dataset">
      </td>
      <td class="datavalues">
      </td>
     </tr>                                        
     <tr>
      <td class="dataset" valign=top>
      Middle Chinese
      </td>                                       
      <td class="datavalues">
       <table>                                    
TEXT;
echo $text;
$mck = $glyphDict['mck'];
foreach ($mck as $reading){
$text = <<<TEXT

        <tr>
         <td>
          <a href="../../eohan/mck/
TEXT;
echo $text;
echo $reading;

$text = <<<TEXT

">
          
TEXT;
echo $text;
echo $reading;

$text = <<<TEXT


          </a>
         </td>
        </tr>
TEXT;
echo $text;
}
$text = <<<TEXT

       </table>
      </td>
     </tr>
     <tr>
      <td class="dataset">                        
      </td>
      <td>
      </td>
     </tr>                
     <tr>
      <td class="dataset" valign=top>             
      Old Chinese
      </td>                          
      <td class="datavalues">
       <table>
TEXT;
echo $text;
$karlgren = $glyphDict['karlgren'];
foreach ($karlgren as $key => $value){
echo $text;
$text = <<<TEXT

        <tr>
         <td>
          <a href="../../eohan/ock/
TEXT;
echo $text;
$karlgrenfinal = $glyphDict['karlgrenfinal'];
echo $karlgrenfinal[$key];
$text = <<<TEXT

"
          </a>
          
TEXT;
echo $text;
echo $karlgren[$key];
$text = <<<TEXT


         </td>
        </tr>
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
TEXT;
echo $text;
include 'bottom.php';
?>