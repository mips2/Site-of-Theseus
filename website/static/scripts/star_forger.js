document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('star-forger-canvas');
    const resetButton = document.getElementById('reset-button');

    let elements = [];

    canvas.addEventListener('click', (event) => {
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        const element = document.createElement('div');
        element.className = 'star-forger-element';
        element.style.left = `${x}px`;
        element.style.top = `${y}px`;
        element.style.backgroundColor = getRandomColor();
        canvas.appendChild(element);

        elements.push(element);
    });

    resetButton.addEventListener('click', () => {
        elements.forEach(element => canvas.removeChild(element));
        elements = [];
    });

    function getRandomColor() {
        const colors = ['#ff6f61', '#6b5b95', '#88b04b', '#f7cac9', '#92a8d1'];
        return colors[Math.floor(Math.random() * colors.length)];
    }
});