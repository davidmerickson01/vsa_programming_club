<html>

<?php
$session = "0";
$other_session = "1";
if ($_SERVER["REQUEST_METHOD"] == "GET") {
    if ($_GET["control"] == "startover") {
        $startover = true;
    }
    else if ($_GET["control"] == "doneplacing") {
        $doneplacing = true;
    }
    if (isset($_GET["session"])) {
        $session = $_GET["session"];
    }
    if (isset($_GET["other_session"])) {
        $other_session = $_GET["other_session"];
    }
}

$game_board_filename = "gamedata/game_board_$session.txt";
$game_state_filename = "gamedata/game_state_$session.txt";

$other_game_board_filename = "gamedata/game_board_$other_session.txt";
$other_game_state_filename = "gamedata/game_state_$other_session.txt";

// game_state: <startover>, place, ready, play

// read or create game board
if ($startover) {
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
else {
    $game_state = file_get_contents($game_state_filename);
    $game_board = unserialize(file_get_contents($game_board_filename));

    $other_game_state = file_get_contents($other_game_state_filename);
    
    if ($doneplacing && $game_state != "play") {
        if ($other_game_state == "placing") {
            $game_state = "ready";
        }
        else {
            $game_state = "play";
        }
    }
    
    if ($other_game_state == "play") {
        $other_game_board = unserialize(file_get_contents($other_game_board_filename));
    }
}

/*
0 = no piece, no guess -> nothing
1 = no piece, wrong guess (aka miss) -> white
2 = piece, no guess -> gray <nothing>
3 = piece, right guess (aka hit) -> red
*/

// modify it
if ($_SERVER["REQUEST_METHOD"] == "GET") {
    $place = $_GET["place"];
    if ($place && $game_state == "place") {
        $row = ord($place[0]) - ord('A');
        $col = $place[1];
        // crude way of handling 10
        if ($place[2] == '0') {
            $col = $col * 10;
        }
        $col = $col - 1; // make it zero-based again
        echo "place $row,$col<br>\n";
        
        if ($game_board[$row][$col] == "2") {
            $game_board[$row][$col] = "0";
        }
        else {
            $game_board[$row][$col] = "2";
        }
    }

    $guess = $_GET["guess"];
    if ($guess && $game_state == "play") {
        // skip over the "E"
        $row = ord($guess[1]) - ord('A');
        $col = $guess[2];
        // crude way of handling 10
        if ($guess[3] == '0') {
            $col = $col * 10;
        }
        $col = $col - 1; // make it zero-based again
        echo "guess: $row,$col<br>\n";
        
        if ($other_game_board[$row][$col] == "2") {
            $other_game_board[$row][$col] = "1";
        }
        else {
            $other_game_board[$row][$col] = "3";
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
<?php if ($game_state == "place") { ?>
//    alert(e.id);
    e.style.backgroundColor = "green";

    myform = document.getElementById("myform");
    // build: <input type='hidden' id='place' value='A1'>
    myform.innerHTML += "<input type='hidden' name='place' value='"+ e.id + "'>";
    myform.submit();
<?php } ?>
}

function guessCoordinates(e) {
<?php if ($game_state == "play") { ?>
//    alert(e.id);
    e.style.backgroundColor = "red";

    myform = document.getElementById("myform");
    // build: <input type='hidden' id='guess' value='A1'>
    myform.innerHTML += "<input type='hidden' name='guess' value='"+ e.id + "'>";
    myform.submit();
<?php } ?>
}

function doneplacing() {
<?php if ($game_state == "place") { ?>
    myform = document.getElementById("myform");
    document.getElementById("control").value = "doneplacing";
    myform.submit();
<?php } ?>
}

function startover() {
    myform = document.getElementById("myform");
    document.getElementById("control").value = "startover";
    myform.submit();
}

</script>

<body>
<h2>state: <?php echo $game_state ?>, other_state: <?php echo $other_game_state ?></h2>
<form id=myform action="battleship6.php" method="get">
<input type='hidden' id="control" name='control' value=''>
Session: <input width=30 type="text" id="session" name="session" value="<?php echo $session ?>">
Other Session: <input width=30 type="text" id="other_session" name="other_session" value="<?php echo $other_session ?>">
<input type=button value="Start Over" onclick="startover()">
</form>

<?php if ($game_state == "place") { ?>
<input type=button value="Done Placing" onclick="doneplacing()">
<?php } ?>

<?php if ($game_state == "ready") { ?>
Other play not ready hit. Wait a bit and hit refresh.<p>
<?php } ?>

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
            echo "<div id='E$row_letters[$r]$col_num' onclick='guessCoordinates(this)'></div>";
        }
    }
    ?>

</div>

<script>
<?php
for ($row=0;$row<10;$row++) {
    for ($col=0;$col<10;$col++) {
        $row_letters = "ABCDEFGHIJ";
        if ($game_board[$row][$col] > 0) {
            $col_name = $col + 1;
            $row_name = $row_letters[$row];
            $id = "$row_name$col_name";
            
            $grid_colors = ["black","white","gray","red"];
            $color = $grid_colors[$game_board[$row][$col]];
            
            echo "//row $row, col $col, id $id<br>\n";
            echo "e = document.getElementById('$id');\n";
            echo "if (e) {e.style.backgroundColor = '$color';}\n";
        }

        if ($other_game_board[$row][$col] > 0) {
            $col_name = $col + 1;
            $row_name = $row_letters[$row];
            // add E to other
            $id = "E$row_name$col_name";
            
            $grid_colors = ["black","white","gray","red"];
            $color = $grid_colors[$other_game_board[$row][$col]];
            
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
