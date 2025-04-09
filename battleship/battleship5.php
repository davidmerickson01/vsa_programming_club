<html>

<?php
$session = "0";
if ($_SERVER["REQUEST_METHOD"] == "GET") {
    if ($_GET["startover"] == "y") {
        $startover = true;
    }
    if ($_GET["session"]) {
        $session = $_GET["session"];
    }
    if ($_GET["doneplacing"] == "y") {
    }
}

$game_board_filename = "gamedata/game_board_$session.txt";
$game_state_filename = "gamedata/game_state_$session.txt";

// states: place, guess

// read or create game board
if (!$startover) {
    $game_state = file_get_contents($game_state_filename);
    $game_board = unserialize(file_get_contents($game_board_filename));
}
if ($game_state == "place") {
}
else {
    $game_state = "place";
    $game_board = [
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

/*
0 = no piece, no guess -> nothing
1 = no piece, wrong guess (aka miss) -> white
2 = piece, no guess -> gray <nothing>
3 = piece, right guess (aka hit) -> red
*/

// modify it
if ($_SERVER["REQUEST_METHOD"] == "GET") {
    $hit = $_GET["hit"];
    if ($hit) {
        $row = ord($hit[0]) - ord('A');
        $col = $hit[1];
        // crude way of handling 10
        if ($hit[2] == '0') {
            $col = $col * 10;
        }
        $col = $col - 1; // make it zero-based again
        echo "row = $row, col = $col<br>\n";
        
        if ($game_state == "place") {
            if ($game_board[$row][$col] == "2") {
                $game_board[$row][$col] = "0";
            }
            else {
                $game_board[$row][$col] = "2";
            }
        }
        else if ($game_state == "guess") {
            if ($game_board[$row][$col] == "0") {
                $game_board[$row][$col] = "1";
            }
            else if ($game_board[$row][$col] == "2") {
                $game_board[$row][$col] = "3";
            }
            else {
                // wasting your turn, you've already guessed
            }
        }
    }
}

// write game board
file_put_contents($game_board_filename, serialize($game_board));
file_put_contents($game_state_filename, $game_state);
?>


<style>
body { 
  background-color: #0686D4;
  background-opacity: 0.5;
  overflow: hidden;
 }
 
.container {
  display: grid;
  grid-template-columns: 50px 50px 50px 50px 50px 50px 50px 50px 50px 50px 50px;
  grid-template-rows: 50px 50px 50px 50px 50px 50px 50px 50px 50px 50px 50px;
  padding: 10px;
}
.container > div {
  border: 1px solid black;
  font-size: 30px;
  text-align: center;
  background-color: #48B6FA;
  display: grid; 
  align-items: center; 
  justify-items: center;
}

.econtainer {
  display: grid;
  grid-template-columns: 50px 50px 50px 50px 50px 50px 50px 50px 50px 50px 50px;
  grid-template-rows: 50px 50px 50px 50px 50px 50px 50px 50px 50px 50px 50px;
  padding: 10px;
  position: absolute;
  right: 50px;
  top: 50px;
}
.econtainer > div {
  border: 1px solid black;
  font-size: 30px;
  text-align: center;
  background-color: #48B6FA;
  display: grid; 
  align-items: center; 
  justify-items: center;
}

</style>

<script>

<?php
// generate JavaScript data structures from php game board
?>

function callCoordinates(e) {
//    alert(e.id);
    e.style.backgroundColor = "green";

    myform = document.getElementById("myform");
    // build: <input type='hidden' id='hit' value='grid1a'>
    myform.innerHTML += "<input type='hidden' name='hit' value='"+ e.id + "'>";
    myform.submit();
}

function doneplacing() {
    myform = document.getElementById("myform");
    myform.innerHTML += "<input type='hidden' name='doneplacing' value='y'>";
    myform.submit();
}

function startover() {
    myform = document.getElementById("myform");
    myform.innerHTML += "<input type='hidden' name='startover' value='y'>";
    myform.submit();
}

</script>

<body>
<h2>State: <?php echo $game_state ?></h2>
<form id=myform action="battleship5.php" method="get">
Session: <input type="text" name="session" value="<?php echo $session ?>">
</form>

<input type=button value="Start Over" onclick="startover()">
<input type=button value="Done Placing" onclick="doneplacing()">

<p>

<div class="container">
    <!-- 1-10 markers -->
    <div></div>
    <div>1</div>
    <div>2</div>
    <div>3</div>
    <div>4</div>
    <div>5</div>
    <div>6</div>
    <div>7</div>
    <div>8</div>
    <div>9</div>
    <div>10</div>
    <?php
    for ($r=0;$r<10;$r++) {
        $row_letters = "ABCDEFGHIJ";
        echo "<div>$row_letters[$r]</div>";
        for ($c=0;$c<10;$c++) {
            $col_num = $c + 1;
            echo "<div id='$row_letters[$r]$col_num' onclick='callCoordinates(this)'></div>";
        }
    }
    ?>
 </div>


<div class="econtainer">
    <!-- 1-10 markers -->
    <div></div>
    <div>1</div>
    <div>2</div>
    <div>3</div>
    <div>4</div>
    <div>5</div>
    <div>6</div>
    <div>7</div>
    <div>8</div>
    <div>9</div>
    <div>10</div>

    <?php
    for ($r=0;$r<10;$r++) {
        $row_letters = "ABCDEFGHIJ";
        echo "<div>$row_letters[$r]</div>";
        for ($c=0;$c<10;$c++) {
            $col_num = $c + 1;
            echo "<div id='E$row_letters[$r]$col_num' onclick='callCoordinates(this)'></div>";
        }
    }
    ?>

</div>

<script>
<?php
for ($row=0;$row<10;$row++) {
    for ($col=0;$col<10;$col++) {
        if ($game_board[$row][$col] > 0) {
            $col_name = $col + 1;
            $row_letters = "ABCDEFGHIJ";
            $row_name = $row_letters[$row];
            $id = "$row_name$col_name";
            
            $grid_colors = ["black","white","gray","red"];
            $color = $grid_colors[$game_board[$row][$col]];
            
            echo "//row $row, col $col, id $id<br>\n";
            echo "e = document.getElementById('$id');\n";
            echo "if (e) {e.style.backgroundColor = '$color';}\n";
        }
    }
}
?>
</script>

</body>
</html>
