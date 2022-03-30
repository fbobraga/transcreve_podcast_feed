<!DOCTYPE html>
<html>
<body>
<form action="busca_resultado.php">
  <label for="fname">Texto de busca nas transcrições dos episódios:</label><br>
  <input type="text" id="texto_busca" name="texto_busca"><br>
  <input type="submit" value="Buscar">
</form>
<br>
<br>
<b>Episódios transcritos:</b><br>
<br>
<?php
exec('ls * | grep -v .php | sort', $retArr, $retVal);

foreach ($retArr as $linha)
    {
        print($linha . '<br>');
    }
?>

</body>
</html>
