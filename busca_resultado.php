<!DOCTYPE html>
<html>
<title>
    Resultados da busca
</title>
<body>
    Resultado da busca:<br>
    <br>
    <?php
    exec('grep -B 1 "' . $_GET['texto_busca'] . '" *', $retArr, $retVal);

    foreach ($retArr as $linha)
        {
            print($linha . '<br>');
        }
    ?>
</body>
</html>
