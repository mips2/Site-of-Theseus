const canvas = document.getElementById('quantumCanvas');
const ctx = canvas.getContext('2d');
const clearCanvasButton = document.getElementById('clearCanvas');
const colorPicker = document.getElementById('colorPicker');
const brushSize = document.getElementById('brushSize');
const quantumEffectButton = document.getElementById('quantumEffect');

let isDrawing = false;
let currentColor = colorPicker.value;
let currentBrushSize = brushSize.value;

canvas.addEventListener('mousedown', () => isDrawing = true);
canvas.addEventListener('mouseup', () => isDrawing = false);
canvas.addEventListener('mousemove', draw);

clearCanvasButton.addEventListener('click', () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
});

colorPicker.addEventListener('input', () => {
    currentColor = colorPicker.value;
});

brushSize.addEventListener('input', () => {
    currentBrushSize = brushSize.value;
});

quantumEffectButton.addEventListener('click', applyQuantumEffect);

function draw(e) {
    if (!isDrawing) return;
    ctx.fillStyle = currentColor;
    ctx.beginPath();
    ctx.arc(e.offsetX, e.offsetY, currentBrushSize / 2, 0, Math.PI * 2);
    ctx.fill();
}

function applyQuantumEffect() {
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;

    for (let i = 0; i < data.length; i += 4) {
        data[i] = 255 - data[i]; // Invert red
        data[i + 1] = 255 - data[i + 1]; // Invert green
        data[i + 2] = 255 - data[i + 2]; // Invert blue
    }

    ctx.putImageData(imageData, 0, 0);
}