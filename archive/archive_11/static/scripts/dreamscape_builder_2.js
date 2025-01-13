const canvas = document.getElementById('dreamCanvas');
const ctx = canvas.getContext('2d');
canvas.width = 800;
canvas.height = 500;

const addCloudBtn = document.getElementById('addCloud');
const addTreeBtn = document.getElementById('addTree');
const addRiverBtn = document.getElementById('addRiver');
const clearCanvasBtn = document.getElementById('clearCanvas');

addCloudBtn.addEventListener('click', () => {
    drawCloud(Math.random() * canvas.width, Math.random() * canvas.height / 2);
});

addTreeBtn.addEventListener('click', () => {
    drawTree(Math.random() * canvas.width, canvas.height - 50);
});

addRiverBtn.addEventListener('click', () => {
    drawRiver();
});

clearCanvasBtn.addEventListener('click', () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
});

function drawCloud(x, y) {
    ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
    ctx.beginPath();
    ctx.arc(x, y, 30, 0, Math.PI * 2);
    ctx.arc(x + 40, y, 40, 0, Math.PI * 2);
    ctx.arc(x + 80, y, 30, 0, Math.PI * 2);
    ctx.fill();
}

function drawTree(x, y) {
    ctx.fillStyle = '#654321';
    ctx.fillRect(x, y, 20, 50);
    ctx.fillStyle = 'green';
    ctx.beginPath();
    ctx.moveTo(x - 30, y);
    ctx.lineTo(x + 50, y);
    ctx.lineTo(x + 10, y - 100);
    ctx.fill();
}

function drawRiver() {
    ctx.fillStyle = 'rgba(0, 119, 190, 0.6)';
    ctx.beginPath();
    ctx.moveTo(0, canvas.height - 50);
    ctx.bezierCurveTo(200, canvas.height - 100, 600, canvas.height - 150, canvas.width, canvas.height - 50);
    ctx.lineTo(canvas.width, canvas.height);
    ctx.lineTo(0, canvas.height);
    ctx.fill();
}