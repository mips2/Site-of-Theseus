function checkRiddle() {
    const answer = document.getElementById('riddle-answer').value.toLowerCase();
    const feedback = document.getElementById('riddle-feedback');
    if (answer === "keyboard") {
        feedback.textContent = "Correct! You've unlocked the next clue.";
        feedback.style.color = "#4caf50";
    } else {
        feedback.textContent = "Incorrect! Try again.";
        feedback.style.color = "#e94560";
    }
}

const canvas = document.getElementById('treasure-map-canvas');
const ctx = canvas.getContext('2d');

canvas.width = 400;
canvas.height = 400;

ctx.fillStyle = '#0f3460';
ctx.fillRect(0, 0, canvas.width, canvas.height);

ctx.strokeStyle = '#e94560';
ctx.lineWidth = 2;

ctx.beginPath();
ctx.moveTo(50, 50);
ctx.lineTo(350, 350);
ctx.stroke();

ctx.beginPath();
ctx.arc(200, 200, 50, 0, Math.PI * 2);
ctx.stroke();

ctx.fillStyle = '#e94560';
ctx.font = '20px Arial';
ctx.fillText('X marks the spot!', 120, 220);