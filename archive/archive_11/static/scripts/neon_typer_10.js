document.addEventListener('DOMContentLoaded', () => {
    const textToType = document.getElementById('text-to-type');
    const typerInput = document.getElementById('typer-input');
    const typerFeedback = document.getElementById('typer-feedback');
    const timeDisplay = document.getElementById('time');
    const accuracyDisplay = document.getElementById('accuracy');
    const wpmDisplay = document.getElementById('wpm');
    const restartBtn = document.getElementById('restart-btn');

    let startTime;
    let timerInterval;
    let totalTyped = 0;
    let correctTyped = 0;

    typerInput.addEventListener('input', () => {
        if (!startTime) {
            startTime = new Date();
            timerInterval = setInterval(updateTime, 100);
        }

        const typedText = typerInput.value;
        const originalText = textToType.textContent;

        totalTyped = typedText.length;
        correctTyped = 0;

        for (let i = 0; i < typedText.length; i++) {
            if (typedText[i] === originalText[i]) {
                correctTyped++;
            }
        }

        const accuracy = (correctTyped / totalTyped) * 100 || 100;
        const wpm = calculateWPM(typedText);

        accuracyDisplay.textContent = accuracy.toFixed(2);
        wpmDisplay.textContent = wpm;

        if (typedText === originalText) {
            clearInterval(timerInterval);
            typerFeedback.textContent = 'Congratulations! You typed it correctly!';
            typerFeedback.style.color = '#00ff00';
        } else {
            typerFeedback.textContent = 'Keep typing...';
            typerFeedback.style.color = '#ff0000';
        }
    });

    restartBtn.addEventListener('click', () => {
        typerInput.value = '';
        typerFeedback.textContent = '';
        timeDisplay.textContent = '0';
        accuracyDisplay.textContent = '100';
        wpmDisplay.textContent = '0';
        startTime = null;
        clearInterval(timerInterval);
    });

    function updateTime() {
        const currentTime = new Date();
        const elapsedTime = (currentTime - startTime) / 1000;
        timeDisplay.textContent = elapsedTime.toFixed(1);
    }

    function calculateWPM(typedText) {
        const words = typedText.split(' ').length;
        const elapsedTime = (new Date()