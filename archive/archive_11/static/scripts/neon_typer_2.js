const neonLetters = document.querySelectorAll('.neon-letter');
const wordInput = document.getElementById('word-input');
const scoreDisplay = document.getElementById('score');
const timerDisplay = document.getElementById('timer');

let score = 0;
let timeLeft = 60;
let currentWord = 'NEON';

wordInput.focus();

wordInput.addEventListener('input', () => {
    const typedWord = wordInput.value.toUpperCase();
    if (typedWord === currentWord) {
        score++;
        scoreDisplay.textContent = `Score: ${score}`;
        wordInput.value = '';
        lightUpNeonSign();
        generateNewWord();
    }
});

function lightUpNeonSign() {
    neonLetters.forEach((letter, index) => {
        setTimeout(() => {
            letter.classList.add('active');
        }, index * 200);
    });

    setTimeout(() => {
        neonLetters.forEach(letter => letter.classList.remove('active'));
    }, 1000);
}

function generateNewWord() {
    const words = ['NEON', 'GLOW', 'TYPE', 'FAST', 'GAME', 'FUN', 'CODE', 'FLASK', 'PYTHON', 'WEB'];
    currentWord = words[Math.floor(Math.random() * words.length)];
    neonLetters.forEach((letter, index) => {
        letter.textContent = currentWord[index];
    });
}

function updateTimer() {
    if (timeLeft > 0) {
        timeLeft--;
        timerDisplay.textContent = `Time: ${timeLeft}`;
    } else {
        clearInterval(timerInterval);
        wordInput.disabled = true;
        alert(`Game Over! Your final score is ${score}`);
    }
}

const timerInterval = setInterval(updateTimer, 1000);

generateNewWord();