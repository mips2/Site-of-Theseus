document.addEventListener('DOMContentLoaded', () => {
    const maze = document.getElementById('maze');
    const resetButton = document.getElementById('reset-button');
    let playerPosition = { x: 0, y: 0 };
    let treasurePosition = { x: 9, y: 9 };

    const generateMaze = () => {
        maze.innerHTML = '';
        for (let y = 0; y < 10; y++) {
            for (let x = 0; x < 10; x++) {
                const cell = document.createElement('div');
                cell.classList.add('cell');
                if (x === playerPosition.x && y === playerPosition.y) {
                    cell.classList.add('player');
                    cell.textContent = 'P';
                } else if (x === treasurePosition.x && y === treasurePosition.y) {
                    cell.classList.add('treasure');
                    cell.textContent = 'T';
                } else if (Math.random() < 0.2) {
                    cell.classList.add('wall');
                } else {
                    cell.classList.add('path');
                }
                maze.appendChild(cell);
            }
        }
    };

    const movePlayer = (dx, dy) => {
        const newX = playerPosition.x + dx;
        const newY = playerPosition.y + dy;
        if (newX >= 0 && newX < 10 && newY >= 0 && newY < 10) {
            const newCell = maze.children[newY * 10 + newX];
            if (!newCell.classList.contains('wall')) {
                playerPosition.x = newX;
                playerPosition.y = newY;
                generateMaze();
                if (playerPosition.x === treasurePosition.x && playerPosition.y === treasurePosition.y) {
                    alert('You found the treasure!');
                    resetMaze();
                }
            }
        }
    };

    const resetMaze = () => {
        playerPosition = { x: 0, y: 0 };
        treasurePosition = { x: 9, y: 9 };
        generateMaze();
    };

    document.addEventListener('keydown', (e) => {
        switch (e.key) {
            case 'ArrowUp':
                movePlayer(0, -1);
                break;
            case 'ArrowDown':
                movePlayer(0, 1);
                break;
            case 'ArrowLeft':
                movePlayer(-1, 0);
                break;
            case 'ArrowRight':
                movePlayer(1, 0);
                break;
        }
    });

    resetButton.addEventListener('click', resetMaze);

    generateMaze();
});