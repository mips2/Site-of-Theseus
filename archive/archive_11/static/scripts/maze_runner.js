document.addEventListener('DOMContentLoaded', () => {
    const player = document.querySelector('.player');
    const maze = document.querySelector('.maze');
    const mazeWidth = maze.offsetWidth;
    const mazeHeight = maze.offsetHeight;
    const playerSize = 20;
    let playerX = 0;
    let playerY = 0;

    const movePlayer = (dx, dy) => {
        const newX = playerX + dx * playerSize;
        const newY = playerY + dy * playerSize;

        if (newX >= 0 && newX <= mazeWidth - playerSize && newY >= 0 && newY <= mazeHeight - playerSize) {
            playerX = newX;
            playerY = newY;
            player.style.left = `${playerX}px`;
            player.style.top = `${playerY}px`;
        }
    };

    document.getElementById('up').addEventListener('click', () => movePlayer(0, -1));
    document.getElementById('left').addEventListener('click', () => movePlayer(-1, 0));
    document.getElementById('down').addEventListener('click', () => movePlayer(0, 1));
    document.getElementById('right').addEventListener('click', () => movePlayer(1, 0));
});