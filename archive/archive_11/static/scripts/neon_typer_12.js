document.addEventListener('DOMContentLoaded', () => {
    const targetText = document.getElementById('targetText').innerText;
    const userInput = document.getElementById('userInput');
    const timeDisplay = document.getElementById('time');
    const accuracyDisplay = document.getElementById('accuracy');

    let startTime, endTime;

    userInput.addEventListener('input', () => {
        if (!startTime) {
            startTime = new Date();
        }

        const currentText = userInput.value;
        const accuracy = calculateAccuracy(targetText, currentText);
        accuracyDisplay.textContent = accuracy;

        if (currentText === targetText) {
            endTime = new Date();
            const timeTaken = (endTime - startTime) / 1000;
            timeDisplay.textContent = timeTaken.toFixed(2);
            userInput.disabled = true;
        }
    });

    function calculateAccuracy(target, input) {
        let correct = 0;
        for (let i = 0; i < input.length; i++) {
            if (input[i] === target[i]) {
                correct++;
            }
        }
        return ((correct / target.length) * 100).toFixed(2);
    }
});