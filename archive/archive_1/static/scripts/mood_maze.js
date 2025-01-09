document.addEventListener("DOMContentLoaded", function() {
    const maze = document.getElementById("maze");
    const mazeForm = document.getElementById("maze-form");
    const timeTakenInput = document.getElementById("time-taken");

    const mazeWidth = 20;
    const mazeHeight = 20;
    const cellSize = 20;

    let playerPosition = { x: 0, y: 0 };
    let endPosition = { x: mazeWidth - 1, y: mazeHeight - 1 };
    let startTime = null;

    function generateMaze() {
        for (let y = 0; y < mazeHeight; y++) {
            for (let x = 0; x < mazeWidth; x++) {
                const cell = document.createElement("div");
                cell.style.left = `${x * cellSize}px`;
                cell.style.top = `${y * cellSize}px`;
                if (x === playerPosition.x && y === playerPosition.y) {
                    cell.classList.add("player");
                } else if (x === endPosition.x && y === endPosition.y) {
                    cell.classList.add("end");
                } else if (Math.random() < 0.2) {
                    cell.classList.add("wall");
                }
                maze.appendChild(cell);
            }
        }
    }

    function movePlayer(dx, dy) {
        const newX = playerPosition.x + dx;
        const newY = playerPosition.y + dy;

        if (newX >= 0 && newX < mazeWidth && newY >= 0 && newY < mazeHeight) {
            const newCell = document.querySelector(`#maze div[style*="left: ${newX * cellSize}px"][style*="top: ${newY * cellSize}px"]`);
            if (!newCell.classList.contains("wall")) {
                const oldCell = document.querySelector(".player");
                oldCell.classList.remove("player");
                newCell.classList.add("player");
                playerPosition = { x: newX, y: newY };

                if (newX === endPosition.x && newY === endPosition.y) {
                    const endTime = new Date();
                    const timeTaken = (endTime - startTime) / 1000;
                    timeTakenInput.value = timeTaken.toFixed(2);
                    mazeForm.submit();
                }
            }
        }
    }

    document.addEventListener("keydown", function(event) {
        if (!startTime) {
            startTime = new Date();
        }
        switch (event.key) {
            case "ArrowUp":
                movePlayer(0, -1);
                break;
            case "ArrowDown":
                movePlayer(0, 1);
                break;
            case "ArrowLeft":
                movePlayer(-1, 0);
                break;
            case "ArrowRight":
                movePlayer(1, 0);
                break;
        }
    });

    generateMaze();
});