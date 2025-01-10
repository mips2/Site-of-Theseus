document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('dreamscapeCanvas');
    const ctx = canvas.getContext('2d');

    const addCloud = document.getElementById('addCloud');
    const addTree = document.getElementById('addTree');
    const addStar = document.getElementById('addStar');
    const clearCanvas = document.getElementById('clearCanvas');

    let isDrawing = false;

    canvas.addEventListener('mousedown', () => isDrawing = true);
    canvas.addEventListener('mouseup', () => isDrawing = false);
    canvas.addEventListener('mousemove', draw);

    addCloud.addEventListener('click', () => addElement('cloud'));
    addTree.addEventListener('click', () => addElement('tree'));
    addStar.addEventListener('click', () => addElement('star'));
    clearCanvas.addEventListener('click', clearCanvasElements);

    function draw(e) {
        if (!isDrawing) return;
        ctx.fillStyle = 'white';
        ctx.beginPath();
        ctx.arc(e.offsetX, e.offsetY, 10, 0, Math.PI * 2);
        ctx.fill();
    }

    function addElement(type) {
        const x = Math.random() * canvas.width;
        const y = Math.random() * canvas.height;

        if (type === 'cloud') {
            ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
            ctx.beginPath();
            ctx.arc(x, y, 30, 0, Math.PI * 2);
            ctx.arc(x + 40, y, 30, 0, Math.PI * 2);
            ctx.arc(x + 20, y - 20, 30, 0, Math.PI * 2);
            ctx.fill();
        } else if (type === 'tree') {
            ctx.fillStyle = 'green';
            ctx.fillRect(x, y, 20, 60);
            ctx.beginPath();
            ctx.arc(x + 10, y - 20, 30, 0, Math.PI * 2);
            ctx.fill();
        } else if (type === 'star') {
            ctx.fillStyle = 'yellow';
            ctx.beginPath();
            ctx.moveTo(x, y - 20);
            ctx.lineTo(x + 20, y + 20);
            ctx.lineTo(x - 20, y + 10);
            ctx.lineTo(x + 20, y + 10);
            ctx.lineTo(x - 20, y + 20);
            ctx.closePath();
            ctx.fill();
        }
    }

    function clearCanvasElements() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
});