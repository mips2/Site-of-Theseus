const words = ["cosmic", "galaxy", "nebula", "star", "planet", "comet", "asteroid", "orbit", "gravity", "universe"];
let score = 0;
let timeLeft = 60;
let timerInterval;
let isGameRunning = false;

const wordDisplay = document.getElementById('word-display');
const typerInput = document.getElementById('typer-input');
const scoreDisplay = document.getElementById('score');
const timerDisplay = document.getElementById('timer');
const startButton = document.getElementById('start-button');
const resetButton = document.getElementById('reset-button');

function getRandomWord() {
    return words[Math.floor(Math.random() * words.length)];
}

function displayWord() {
    wordDisplay.textContent = getRandomWord();
}

function updateScore() {
    score++;
    scoreDisplay.textContent = score;
}

function updateTimer() {
    timeLeft--;
    timerDisplay.textContent = timeLeft;
    if (timeLeft <= 0) {
        endGame();
    }
}

function startGame() {
    if (isGameRunning) return;
    isGameRunning = true;
    score = 0;
    timeLeft = 60;
    scoreDisplay.textContent = score;
    timerDisplay.textContent = timeLeft;
    displayWord();
    typerInput.value = '';
    typerInput.focus();
    timerInterval = setInterval(updateTimer, 1000);
}

function endGame() {
    clearInterval(timerInterval);
    isGameRunning = false;
    alert(`Game Over! Your final score is ${score}`);
}

function resetGame() {
    clearInterval(timerInterval);
    isGameRunning = false;
    score = 0;
    timeLeft = 60;
    scoreDisplay.textContent = score;
    timerDisplay.textContent = timeLeft;
    wordDisplay.textContent = 'Type the words below as fast as you can!';
    typerInput.value = '';
}

typerInput.addEventListener('input', () => {
    if (typerInput.value === wordDisplay.textContent) {
        updateScore();
        displayWord();
        typerInput.value = '';
    }
});

startButton.addEventListener('click', startGame);
resetButton.addEventListener('click', resetGame);