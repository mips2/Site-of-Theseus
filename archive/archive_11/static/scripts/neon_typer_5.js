const words = ["cosmic", "nebula", "galaxy", "quantum", "stellar", "orbit", "pulsar", "quasar", "eclipse", "supernova"];
let score = 0;
let time = 60;
let isPlaying;

const wordDisplay = document.getElementById('word-display');
const wordInput = document.getElementById('word-input');
const scoreDisplay = document.getElementById('score');
const timeDisplay = document.getElementById('time');
const message = document.getElementById('message');

function init() {
    showWord(words);
    wordInput.addEventListener('input', startMatch);
    setInterval(countdown, 1000);
    setInterval(checkStatus, 50);
}

function showWord(words) {
    const randomIndex = Math.floor(Math.random() * words.length);
    wordDisplay.innerHTML = words[randomIndex];
}

function startMatch() {
    if (matchWords()) {
        isPlaying = true;
        time = 60;
        showWord(words);
        wordInput.value = '';
        score++;
    }
    scoreDisplay.innerHTML = score;
}

function matchWords() {
    if (wordInput.value === wordDisplay.innerHTML) {
        message.innerHTML = 'Correct!!!';
        return true;
    } else {
        message.innerHTML = '';
        return false;
    }
}

function countdown() {
    if (time > 0) {
        time--;
    } else if (time === 0) {
        isPlaying = false;
    }
    timeDisplay.innerHTML = time;
}

function checkStatus() {
    if (!isPlaying && time === 0) {
        message.innerHTML = 'Game Over!!!';
        score = 0;
    }
}

window.onload = init;