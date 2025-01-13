document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('quantumCanvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 800;
    canvas.height = 600;

    let painting = false;
    let brushColor = '#ff0000';
    let brushSize = 10;

    const colorPicker = document.getElementById('colorPicker');
    const brushSizeInput = document.getElementById('brushSize');
    const clearCanvasButton = document.getElementById('clearCanvas');
    const saveArtButton = document.getElementById('saveArt');
    const artGallery = document.getElementById('artGallery');

    function startPosition(e) {
        painting = true;
        draw(e);
    }

    function endPosition() {
        painting = false;
        ctx.beginPath();
    }

    function draw(e) {
        if (!painting) return;

        ctx.lineWidth = brushSize;
        ctx.lineCap = 'round';
        ctx.strokeStyle = brushColor;

        ctx.lineTo(e.offsetX, e.offsetY);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(e.offsetX, e.offsetY);
    }

    canvas.addEventListener('mousedown', startPosition);
    canvas.addEventListener('mouseup', endPosition);
    canvas.addEventListener('mousemove', draw);

    colorPicker.addEventListener('input', () => {
        brushColor = colorPicker.value;
    });

    brushSizeInput.addEventListener('input', () => {
        brushSize = brushSizeInput.value;
    });

    clearCanvasButton.addEventListener('click', () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    });

    saveArtButton.addEventListener('click', () => {
        const dataURL = canvas.toDataURL();
        const img = document.createElement('img');
        img.src = dataURL;
        artGallery.appendChild(img);
    });
});