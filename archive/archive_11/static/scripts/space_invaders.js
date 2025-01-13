const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const playerWidth = 50;
const playerHeight = 20;
const playerSpeed = 7;
const bulletSpeed = 5;
const enemyRows = 3;
const enemyColumns = 8;
const enemyWidth = 40;
const enemyHeight = 30;
const enemyPadding = 20;
const enemyOffsetTop = 30;
const enemyOffsetLeft = 30;

let player = {
    x: canvas.width / 2 - playerWidth / 2,
    y: canvas.height - playerHeight - 10,
    dx: 0
};

let bullets = [];
let enemies = [];
let gameOver = false;
let score = 0;

function drawPlayer() {
    ctx.fillStyle = '#00ffcc';
    ctx.fillRect(player.x, player.y, playerWidth, playerHeight);
}

function drawBullets() {
    ctx.fillStyle = '#ff00cc';
    bullets.forEach(bullet => {
        ctx.fillRect(bullet.x, bullet.y, 5, 10);
    });
}

function drawEnemies() {
    ctx.fillStyle = '#ffcc00';
    enemies.forEach(enemy => {
        if (enemy.active) {
            ctx.fillRect(enemy.x, enemy.y, enemyWidth, enemyHeight);
        }
    });
}

function updatePlayer() {
    player.x += player.dx;
    if (player.x < 0) player.x = 0;
    if (player.x + playerWidth > canvas.width) player.x = canvas.width - playerWidth;
}

function updateBullets() {
    bullets.forEach((bullet, index) => {
        bullet.y -= bulletSpeed;
        if (bullet.y < 0) {
            bullets.splice(index, 1);
        }
    });
}

function updateEnemies() {
    let allEnemiesDead = true;
    enemies.forEach(enemy => {
        if (enemy.active) {
            allEnemiesDead = false;
            enemy.x += enemy.dx;
            if (enemy.x + enemyWidth > canvas.width || enemy.x < 0) {
                enemy.dx *= -1;
                enemy.y += enemyOffsetTop;
            }
        }
    });
    if (allEnemiesDead) {
        resetEnemies();
    }
}

function checkCollisions() {
    bullets.forEach((bullet, bulletIndex) => {
        enemies.forEach((enemy, enemyIndex) => {
            if (enemy.active && bullet.x < enemy.x + enemyWidth &&
                bullet.x + 5 > enemy.x &&
                bullet.y < enemy.y + enemyHeight &&
                bullet.y + 10 > enemy.y) {
                bullets.splice(bulletIndex, 1);
                enemy.active = false;
                score += 10;
            }
        });
    });
}

function resetEnemies() {
    enemies = [];
    for (let row = 0; row < enemyRows; row++) {
        for (let col = 0; col < enemyColumns; col++) {
            enemies.push({
                x: col * (enemyWidth + enemyPadding) + enemyOffsetLeft,
                y: row * (enemyHeight + enemyPadding) + enemyOffsetTop,
                dx: 2,
                active: true
            });
        }
    }
}

function drawScore() {
    ctx.fillStyle = '#fff';
    ctx.font = '20px Arial';
    ctx.fillText(`Score: ${score}`, 10, 30);
}

function drawGameOver() {
    ctx.fillStyle = '#fff';
    ctx.font = '40px Arial';
    ctx.fillText('Game Over!', canvas.width / 2 - 100, canvas.height / 2);
}

function gameLoop() {
    if (gameOver) {
        drawGameOver();
        return;
    }
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawPlayer();
    drawBullets();
    drawEnemies();
    updatePlayer();
    updateBullets();
    updateEnemies();
    checkCollisions();
    drawScore();
    requestAnimationFrame(gameLoop);
}

document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') {
        player.dx = -playerSpeed;
    } else if (e.key === 'ArrowRight') {
        player.dx = playerSpeed;
    } else if (e.key === ' ' && !gameOver) {
        bullets.push({ x: player.x + playerWidth / 2 - 2.5, y: player.y });
    }
});

document.addEventListener('keyup', (e) => {
    if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
        player.dx = 0;
    }
});

resetEnemies();
gameLoop();