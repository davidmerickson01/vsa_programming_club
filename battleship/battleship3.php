<html>

<?php
$session = "0";
$game_filename = "game_$session.txt";

// read or create game board
$str = file_get_contents($game_filename);
if ($str) {
    echo "<h1>Continue Game:$session</h1>\n";
    $game_struct = unserialize($str);
}
else {
    echo "<h1>New Game:$session</h1>\n";
    $game_struct = [
    "0000000000",
    "0000000000",
    "0000000000",
    "0000000000",
    "0000000000",
    "0000000000",
    "0000000000",
    "0000000000",
    "0000000000",
    "0000000000" ];
}

// modify it
if ($_SERVER["REQUEST_METHOD"] == "GET") {
    $hit = $_GET["hit"];
    if ($hit) {
        $col = $hit[4] - 1;
        $row = intval($hit[5]) - intval('a');
        echo "row = $row, col = $col<br>\n";
        $game_struct[$row][$col] = "1";
    }
}

// write game board
file_put_contents($game_filename, serialize($game_struct));
?>


<style>
.container {
  display: grid;
  grid-template-columns: auto auto auto auto auto auto auto auto auto auto;
  background-color: dodgerblue;
  padding: 10px;
}
.container > div {
  background-color: #f1f1f1;
  border: 1px solid black;
  padding: 10px;
  font-size: 30px;
  text-align: center;
}
</style>

<script>

<?php
// generate JavaScript data structures from php game board
?>

var prev_e;
var prev_e_backgroundColor;

function gridclick(e) {
//    alert(e.id);
    if (prev_e) {
        prev_e.style.backgroundColor = prev_e_backgroundColor;
    }
    prev_e = e;
    prev_e_backgroundColor = e.style.backgroundColor;
    e.style.backgroundColor = "green";

    // build: <input type='hidden' id='hit' value='grid1a'>
    document.getElementById("myform").innerHTML = "<input type='hidden' name='hit' value='"+ e.id + "'>";
}

function submitform() {
    document.getElementById("myform").submit();
}

</script>

<!-- hidden form -->
<form id=myform action="battleship3.php" method="get">
</form>
<input type=button onclick="submitform()" value=Submit>

<body>

<h1>Your shots</h1>

<div class="container">
  <div id=grid1a onclick="gridclick(this)">1a</div>
  <div id=grid2a onclick="gridclick(this)">2a</div>
  <div id=grid3a onclick="gridclick(this)">3a</div>  
  <div>4a</div>
  <div>5a</div>
  <div>6a</div>  
  <div>7a</div>
  <div>8a</div>
  <div>9a</div>
  <div>10a</div>
  
  <div>1b</div>  
  <div>2b</div>
  <div>3b</div>
  <div>4b</div>  
  <div>5b</div>
  <div>6b</div>
  <div>7b</div>
  <div>8b</div>
  <div>9b</div>
   <div>10b</div>
    
  <div>1c</div>
  <div>2c</div>  
  <div>3c</div>
  <div>4c</div>
  <div>5c</div>  
  <div>6c</div>
  <div>7c</div>
  <div>8c</div>
  <div>9c</div>
  <div>10c</div> 
  
  <div>1d</div>
  <div>2d</div>
  <div>3d</div>  
  <div>4d</div>
  <div>5d</div>
  <div>6d</div>
  <div>7d</div>
  <div>8d</div>
  <div>9d</div>
  <div>10d</div>
  
  <div>1e</div>  
  <div>2e</div>
  <div>3e</div>
  <div>4e</div>  
  <div>5e</div>
  <div>6e</div>
  <div>7e</div>
  <div>8e</div>
  <div>9e</div>  
  <div>10e</div>
  
  <div>1f</div>
  <div>2f</div>  
  <div>3f</div>
  <div>4f</div>
  <div>5f</div>
  <div>6f</div>
  <div>7f</div>
  <div>8f</div>
  <div>9f</div>
  <div>10f</div> 
  
  <div>1g</div>
  <div>2g</div>
  <div>3g</div>  
  <div>4g</div>
  <div>5g</div>
  <div>6g</div>
  <div>7g</div>
  <div>8g</div>  
  <div>9g</div>
  <div>10g</div>
  
  <div>1h</div>  
  <div>2h</div>
  <div>3h</div>
  <div>4h</div>
  <div>5h</div>
  <div>6h</div>
  <div>7h</div>
  <div>8h</div>
  <div>9h</div>  
  <div>10h</div>
  
  
  <div>1i</div>
  <div>2i</div>  
  <div>3i</div>
  <div>4i</div>
  <div>5i</div>
  <div>6i</div>
  <div>7i</div>  
  <div>8i</div>
  <div>9i</div>
  <div>10i</div>
  
  <div>1j</div>
  <div>2j</div>
  <div>3j</div>
  <div>4j</div>
  <div>5j</div>
  <div>6j</div>
  <div>7j</div>
  <div>9j</div>
  <div>9j</div>
 <div>10j</div>
</div>

<h1>Shots Received</h1>

<div class="container">
  <div>1a</div>
  <div>2a</div>
  <div>3a</div>  
  <div>4a</div>
  <div>5a</div>
  <div>6a</div>  
  <div>7a</div>
  <div>8a</div>
  <div>9a</div>
  <div>10a</div>
  
  <div>1b</div>  
  <div>2b</div>
  <div>3b</div>
  <div>4b</div>  
  <div>5b</div>
  <div>6b</div>
  <div>7b</div>
  <div>8b</div>
  <div>9b</div>
   <div>10b</div>
    
  <div>1c</div>
  <div>2c</div>  
  <div>3c</div>
  <div>4c</div>
  <div>5c</div>  
  <div>6c</div>
  <div>7c</div>
  <div>8c</div>
  <div>9c</div>
  <div>10c</div> 
  
  <div>1d</div>
  <div>2d</div>
  <div>3d</div>  
  <div>4d</div>
  <div>5d</div>
  <div>6d</div>
  <div>7d</div>
  <div>8d</div>
  <div>9d</div>
  <div>10d</div>
  
  <div>1e</div>  
  <div>2e</div>
  <div>3e</div>
  <div>4e</div>  
  <div>5e</div>
  <div>6e</div>
  <div>7e</div>
  <div>8e</div>
  <div>9e</div>  
  <div>10e</div>
  
  <div>1f</div>
  <div>2f</div>  
  <div>3f</div>
  <div>4f</div>
  <div>5f</div>
  <div>6f</div>
  <div>7f</div>
  <div>8f</div>
  <div>9f</div>
  <div>10f</div> 
  
  <div>1g</div>
  <div>2g</div>
  <div>3g</div>  
  <div>4g</div>
  <div>5g</div>
  <div>6g</div>
  <div>7g</div>
  <div>8g</div>  
  <div>9g</div>
  <div>10g</div>
  
  <div>1h</div>  
  <div>2h</div>
  <div>3h</div>
  <div>4h</div>
  <div>5h</div>
  <div>6h</div>
  <div>7h</div>
  <div>8h</div>
  <div>9h</div>  
  <div>10h</div>
  
  
  <div>1i</div>
  <div>2i</div>  
  <div>3i</div>
  <div>4i</div>
  <div>5i</div>
  <div>6i</div>
  <div>7i</div>  
  <div>8i</div>
  <div>9i</div>
  <div>10i</div>
  
  <div>1j</div>
  <div>2j</div>
  <div>3j</div>
  <div>4j</div>
  <div>5j</div>
  <div>6j</div>
  <div>7j</div>
  <div>9j</div>
  <div>9j</div>
 <div>10j</div>
</div>

<script>
<?php
for ($row=0;$row<10;$row++) {
    for ($col=0;$col<10;$col++) {
        if ($game_struct[$row][$col] == 1) {
            $col_name = $col + 1;
            $row_letters = "abcdefghij";
            $row_name = $row_letters[$row];
            $id = "grid$col_name$row_name";
            //echo "//row $row, col $col, id $id<br>\n";
            echo "e = document.getElementById('$id');\n";
            echo "if (e) {e.style.backgroundColor = 'yellow';}\n";
        }
    }
}
?>
</script>

</body>
</html>
