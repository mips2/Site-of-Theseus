document.addEventListener('DOMContentLoaded', () => {
    const textToType = document.getElementById('text-to-type');
    const typingInput = document.getElementById('typing-input');
    const timerDisplay = document.getElementById('timer');
    const resultDisplay = document.getElementById('result');
    const restartButton = document.getElementById('restart-button');

    let startTime, endTime, timerInterval;

    typingInput.addEventListener('input', () => {
        if (!startTime) {
            startTime = new Date();
            timerInterval = setInterval(updateTimer, 10);
        }

        if (typingInput.value === textToType.textContent) {
            endTime = new Date();
            clearInterval(timerInterval);
            const timeTaken = (endTime - startTime) / 1000;
            resultDisplay.textContent = `You finished in ${timeTaken.toFixed(2)} seconds!`;
            typingInput.disabled = true;
        }
    });

    restartButton.addEventListener('click', () => {
        typingInput.value = '';
        typingInput.disabled = false;
        startTime = null;
        endTime = null;
        clearInterval(timerInterval);
        timerDisplay.textContent = 'Time: 0.00s';
        resultDisplay.textContent = '';
    });

    function updateTimer() {
        const currentTime = new Date();
        const timeElapsed = (currentTime - startTime) / 1000;
        timerDisplay.textContent = `Time: ${timeElapsed.toFixed(2)}s`;
    }
});