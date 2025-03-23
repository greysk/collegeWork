function getRandomInt(min, max) {
    // Copied from https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random#getting_a_random_integer_between_two_values
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1) + min);
}

function roll() {
    // let dice = [[1, '\u9856'], [2, '\u9857'], [3, '\u9858'], [4, '\u9859'], [5, '\u9860'], [6, '\u9861']];
    let dice = [[1, '\u2680'], [2, '\u2681'], [3, '\u2682'], [4, '\u2683'], [5, '\u2684'], [6, '\u2685']];

    return dice[getRandomInt(0, 5)];
}

let myRoll = roll();
let yourRoll = roll();

function playGame() {
    document.getElementById('yourdice').textContent = yourRoll[1];
    let gameResult = document.getElementById('gameResult');

    if (yourRoll[0] > myRoll[0]) {
        gameResult.textContent = "You Win!";
        gameResult.style = "color: aliceblue";
    }
    else {
        gameResult.textContent = "You lost.";
        gameResult.style = "color:aliceblue";
    }
}

function listen(){
    // Roll dice for user's opponent.
    document.getElementById('mydice').textContent = myRoll[1];

    /*Listen for a click on yourdice text.*/
    document.getElementById('yourdice').addEventListener('click', playGame);
}

// Wait until webpage is loaded before attempting to get Free Response input element.
document.addEventListener('DOMContentLoaded', listen);
