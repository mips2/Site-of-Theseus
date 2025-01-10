document.addEventListener('DOMContentLoaded', () => {
    const quoteElement = document.getElementById('quote');
    const inputBox = document.getElementById('input-box');
    const timerElement = document.getElementById('timer');
    const accuracyElement = document.getElementById('accuracy');
    const scoreElement = document.getElementById('score');
    const restartBtn = document.getElementById('restart-btn');

    let startTime, endTime, timerInterval;
    let currentQuote = '';
    let correctChars = 0;

    const quotes = [
        "The cosmos is within us. We are made of star-stuff.",
        "Look up at the stars and not down at your feet.",
        "The universe is not only stranger than we imagine, it is stranger than we can imagine.",
        "We are a way for the cosmos to know itself.",
        "The nitrogen in our DNA, the calcium in our teeth, the iron in our blood were made in the interiors of collapsing stars."
    ];

    function getRandomQuote() {
        return quotes[Math.floor(Math.random() * quotes.length)];
    }

    function startGame() {
        currentQuote = getRandomQuote();
        quoteElement.textContent = currentQuote;
        inputBox.value = '';
        inputBox.disabled = false;
        inputBox.focus();
        startTime = new Date();
        timerInterval = setInterval(updateTimer, 1000);
        correctChars = 0;
        updateStats();
    }

    function updateTimer() {
        const currentTime = new Date();
        const elapsedTime = Math.floor((currentTime - startTime) / 1000);
        timerElement.textContent = elapsedTime;
    }

    function updateStats() {
        const typedChars = inputBox.value.length;
        const accuracy = typedChars === 0 ? 100 : Math.floor((correctChars / typedChars) * 100);
        accuracyElement.textContent = accuracy;
        scoreElement.textContent = correctChars;
    }

    function checkInput() {
        const typedText = inputBox.value;
        let correctText = '';
        for (let i = 0; i < typedText.length; i++) {
            if (typedText[i] === currentQuote[i]) {
                correctText += typedText[i];
                correctChars++;
            } else {
                break;
            }
        }
        if (typedText === currentQuote) {
            clearInterval(timerInterval);
            inputBox.disabled = true;
            alert(`Congratulations! You completed the quote in ${timerElement.textContent} seconds with ${accuracyElement.textContent}% accuracy.`);
        }
        updateStats();
    }

    inputBox.addEventListener('input', checkInput);
    restartBtn.addEventListener('click', startGame);

    startGame();
});