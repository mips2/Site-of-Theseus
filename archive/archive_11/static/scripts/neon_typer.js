const wordDisplay = document.getElementById('word-display');
const wordInput = document.getElementById('word-input');
const scoreDisplay = document.getElementById('score-display');

let score = 0;
let currentWord = '';

const words = [
    'neon', 'cyber', 'pulse', 'glow', 'flux', 'laser', 'grid', 'code', 'byte', 'pixel',
    'synth', 'wave', 'data', 'link', 'node', 'core', 'chip', 'disk', 'port', 'zone'
];

function getRandomWord() {
    return words[Math.floor(Math.random() * words.length)];
}

function updateWord() {
    currentWord = getRandomWord();
    wordDisplay.textContent = currentWord;
}

function updateScore() {
    score++;
    scoreDisplay.textContent = `Score: ${score}`;
}

function checkInput() {
    if (wordInput.value === currentWord) {
        updateScore();
        wordInput.value = '';
        updateWord();
    }
}

wordInput.addEventListener('input', checkInput);

updateWord();