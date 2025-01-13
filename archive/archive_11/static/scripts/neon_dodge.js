document.addEventListener('DOMContentLoaded', () => {
    const player = document.getElementById('player');
    const obstacle = document.getElementById('obstacle');
    const scoreDisplay = document.getElementById('score');
    const startBtn = document.getElementById('start-btn');
    let score = 0;
    let gameInterval;

    startBtn.addEventListener('click', startGame);

    function startGame() {
        score = 0;
        scoreDisplay.textContent = score;
        startBtn.disabled = true;
        obstacle.style.top = '-50px';
        gameInterval = setInterval(moveObstacle, 20);
        document.addEventListener('mousemove', movePlayer);
    }

    function movePlayer(e) {
        const gameArea = document.querySelector('.game-area');
        const gameAreaRect = gameArea.getBoundingClientRect();
        const mouseX = e.clientX - gameAreaRect.left;
        player.style.left = `${mouseX - player.offsetWidth / 2}px`;
    }

    function moveObstacle() {
        const obstacleTop = parseInt(obstacle.style.top);
        if (obstacleTop > 400) {
            score++;
            scoreDisplay.textContent = score;
            obstacle.style.top = '-50px';
            obstacle.style.left = `${Math.random() * 250}px`;
        } else {
            obstacle.style.top = `${obstacleTop + 5}px`;
        }
        checkCollision();
    }

    function checkCollision() {
        const playerRect = player.getBoundingClientRect();
        const obstacleRect = obstacle.getBoundingClientRect();
        if (
            playerRect.left < obstacleRect.right &&
            playerRect.right > obstacleRect.left &&
            playerRect.top < obstacleRect.bottom &&
            playerRect.bottom > obstacleRect.top
        ) {
            endGame();
        }
    }

    function endGame() {
        clearInterval(gameInterval);
        startBtn.disabled = false;
        alert(`Game Over! Your score is ${score}`);
    }
});