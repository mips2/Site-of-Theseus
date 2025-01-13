const words = ["neon", "glow", "typer", "flash", "light", "pulse", "radiant", "vivid", "luminous", "bright"];
let currentWord = "";
let score = 0;
let time = 60;
let timerInterval;

const neonInput = document.getElementById("neon-input");
const scoreDisplay = document.getElementById("score");
const timerDisplay = document.getElementById("timer");

function getRandomWord() {
    return words[Math.floor(Math.random() * words.length)];
}

function updateWord() {
    currentWord = getRandomWord();
    document.querySelector(".neon-text").textContent = `Type: ${currentWord}`;
}

function startGame() {
    updateWord();
    neonInput.value = "";
    score = 0;
    time = 60;
    scoreDisplay.textContent = score;
    timerDisplay.textContent = time;
    neonInput.focus();
    timerInterval = setInterval(updateTimer, 1000);
}

function updateTimer() {
    time--;
    timerDisplay.textContent = time;
    if (time <= 0) {
        clearInterval(timerInterval);
        alert(`Game Over! Your score is ${score}`);
        startGame();
    }
}

neonInput.addEventListener("input", (e) => {
    if (e.target.value === currentWord) {
        score++;
        scoreDisplay.textContent = score;
        updateWord();
        e.target.value = "";
    }
});

startGame();