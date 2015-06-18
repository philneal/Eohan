<?php
include 'top.php';
$text = <<<TEXT
<div class="text">
    <h2>About this site</h2>
    <p><br>
      This website is the outcome of a personal software project inspired by
      three books:<br>
      <br>
      <span style="font-style: italic;">Grammata Serica Recensa</span> by
      Bernhard Karlgren<br>
      <span style="font-style: italic;">Middle Chinese</span> by Edwin M
      Pulleyblank<br>
      <span style="font-style: italic;">Old Chinese</span> by William S Baxter<br>
      <br>
      Bernhard Karlgren and his successors penetrated the veil of an ideographic
      script to trace the evolution of Chinese as a spoken language from the
      earliest times to the present day. This site is meant as a tribute to
      their achievement and an aid to understanding it.</p>
    <h4>"All I see is meaningless Chinese characters surrounded by meaningless
      labels."</h4>
    <p>
      The Chinese texts are historical dictionaries giving the pronunciations of
      thousands of ideograms, using ideograms to do so. They constitute a data
      set from which it is possible to deduce the approximate sound of Chinese
      as far back as 3000 years ago. Actually solving this seemingly circular
      puzzle was the life work of great scholars. Given their solutions it is
      possible to turn the evidence and arguments into algorithms and reproduce
      their work (imperfectly) in software. That is the aim of this project. The
      Roman text you see is modern phonetic notation and was generated directly
      from the Chinese text you see.</p>
    <h4>"Mistakes, mistakes! Do you actually know Chinese?"</h4>
    <p>
      I am a language and computing hobbyist. I do not know Chinese and I know
      this site contains mistakes. It should not be cited in serious scholarship
      and the forms in it should not be attributed to Karlgren, Pulleyblank or
      Baxter. It is proof of concept: it demonstrates that it is possible to
      autogenerate Middle and Old Chinese from sources in the public
      domain. I have gone about as far as I can and anyone wishing to take it
      over and improve on it is welcome to do so.</p>
    <h4>"You don't know Chinese?"</h4>
    <p>
      No, although I know a good many characters and the principles of the
      script. My hobby is historical linguistics and I know plenty about plenty
      of languages I do not know. I could easily write several pages of fact
      about Sanskrit or Arabic, though I do not understand either language.
      Historical linguists, amateur and professional, are like that.</p>
    <h4>"What did you spend more than a year doing?"</h4>
    <p>
      Digitising texts I needed and proofreading them against the originals.
      Studying the work of Karlgren, Pulleyblank and Baxter and converting it
      into algorithms. Writing code to implement the algorithms and designing a
      database to hold the output. Writing an app to wrap the data in hypertext
      and&nbsp; publish it as dynamic web pages.</p>
    <h4>"Why is it important?"</h4>
    <p>
      The ongoing reconstruction of Old Chinese is an achievement comparable to
      the reconstruction of Indo-European in the nineteenth century, and it
      proves historical linguistics to be a science. It has emerged that the
      oldest form of Chinese lacked tones, possessed inflections and may be
      related to Indo-European. It is a window into prehistory and much more
      remains to be discovered. </p>

TEXT;
echo $text;
include 'bottom.php';
?>