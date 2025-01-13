const words = ["cosmic", "galaxy", "nebula", "quantum", "stellar", "orbit", "pulsar", "quasar", "eclipse", "supernova"];
let currentWord = "";
let score = 0;
let timeLeft = 60;
let timer;

const typerText = document.getElementById("typer-text");
const typerInput = document.getElementById("typer-input");
const scoreDisplay = document.getElementById("score");
const timerDisplay = document.getElementById("timer");

function getRandomWord() {
    return words[Math.floor(Math.random() * words.length)];
}

function updateWord() {
    currentWord = getRandomWord();
    typerText.textContent = currentWord;
}

function updateScore() {
    score++;
    scoreDisplay.textContent = score;
}

function updateTimer() {
    timeLeft--;
    timerDisplay.textContent = timeLeft;
    if (timeLeft <= 0) {
        clearInterval(timer);
        alert(`Game Over! Your final score is ${score}`);
        resetGame();
    }
}

function resetGame() {
    score = 0;
    timeLeft = 60;
    scoreDisplay.textContent = score;
    timerDisplay.textContent = timeLeft;
    updateWord();
    typerInput.value = "";
    timer = setInterval(updateTimer, 1000);
}

typerInput.addEventListener("input", () => {
    if (typerInput.value === currentWord) {
        updateScore();
        updateWord();
        typerInput.value = "";
    }
});

resetGame();