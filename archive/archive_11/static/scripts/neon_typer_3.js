const words = ["neon", "typer", "cyber", "pulse", "glow", "matrix", "code", "hack", "byte", "data"];
let currentWord = "";
let score = 0;
let time = 60;
let timerInterval;

const wordDisplay = document.getElementById("word-display");
const wordInput = document.getElementById("word-input");
const scoreDisplay = document.getElementById("score");
const timerDisplay = document.getElementById("timer");

function getRandomWord() {
    return words[Math.floor(Math.random() * words.length)];
}

function updateWordDisplay() {
    currentWord = getRandomWord();
    wordDisplay.textContent = currentWord;
}

function updateScore() {
    score++;
    scoreDisplay.textContent = `Score: ${score}`;
}

function updateTimer() {
    time--;
    timerDisplay.textContent = `Time: ${time}`;
    if (time <= 0) {
        clearInterval(timerInterval);
        alert(`Game Over! Your final score is ${score}`);
        wordInput.disabled = true;
    }
}

wordInput.addEventListener("input", () => {
    if (wordInput.value === currentWord) {
        updateScore();
        wordInput.value = "";
        updateWordDisplay();
    }
});

function startGame() {
    updateWordDisplay();
    timerInterval = setInterval(updateTimer, 1000);
}

startGame();