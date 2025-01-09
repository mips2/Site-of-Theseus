document.addEventListener('DOMContentLoaded', () => {
    const tiles = document.querySelectorAll('.quantum-tile');
    const leapButton = document.getElementById('quantum-leap-button');
    const resultDisplay = document.getElementById('quantum-result');

    tiles.forEach(tile => {
        tile.addEventListener('click', () => {
            tile.dataset.state = (parseInt(tile.dataset.state) + 1) % 4;
            tile.style.background = `hsl(${90 * tile.dataset.state}, 70%, 50%)`;
        });
    });

    leapButton.addEventListener('click', () => {
        const states = Array.from(tiles).map(tile => tile.dataset.state);
        if (states.every(state => state === '0')) {
            resultDisplay.textContent = 'You successfully leaped through the quantum realm!';
        } else {
            resultDisplay.textContent = 'The quantum realm is unstable. Try again!';
        }
    });
});