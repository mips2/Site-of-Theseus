document.addEventListener('DOMContentLoaded', () => {
    const typingText = document.getElementById('typing-text');
    const typingInput = document.getElementById('typing-input');
    const timerDisplay = document.getElementById('timer');
    const scoreDisplay = document.getElementById('score');
    const startButton = document.getElementById('start-button');

    let timer = 0;
    let score = 0;
    let interval;

    const phrases = [
        "Explore the cosmos with Neon Typer 7!",
        "Type fast to unlock the secrets of the universe.",
        "The stars are waiting for your words.",
        "Challenge your typing skills in this cosmic adventure.",
        "Every keystroke brings you closer to the stars."
    ];

    function startGame() {
        typingInput.value = '';
        score = 0;
        timer = 0;
        scoreDisplay.textContent = score;
        timerDisplay.textContent = timer;
        typingInput.disabled = false;
        typingInput.focus();
        startButton.disabled = true;
        updatePhrase();
        interval = setInterval(updateTimer, 1000);
    }

    function updateTimer() {
        timer++;
        timerDisplay.textContent = timer;
    }

    function updatePhrase() {
        const randomPhrase = phrases[Math.floor(Math.random() * phrases.length)];
        typingText.textContent = randomPhrase;
    }

    function checkInput() {
        if (typingInput.value === typingText.textContent) {
            score++;
            scoreDisplay.textContent = score;
            typingInput.value = '';
            updatePhrase();
        }
    }

    typingInput.addEventListener('input', checkInput);
    startButton.addEventListener('click', startGame);
});