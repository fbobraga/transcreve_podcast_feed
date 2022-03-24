<!DOCTYPE html>
<html>
<title>
    Resultados da busca
</title>
<body>
    <?php
    exec('grep -B 1 "' . . '" *', $retArr, $retVal);

    foreach ($retArr as $linha)
        {
            print($linha . '<br>');
        }
    ?>
</body>
</html>
