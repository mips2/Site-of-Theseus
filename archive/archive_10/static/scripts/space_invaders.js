const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const player = {
    x: canvas.width / 2 - 25,
    y: canvas.height - 60,
    width: 50,
    height: 50,
    color: '#00ff00',
    speed: 7,
    dx: 0
};

const bullets = [];
const enemies = [];
const enemyRows = 3;
const enemyColumns = 8;
const enemyWidth = 50;
const enemyHeight = 50;
const enemyPadding = 20;
let enemyDirection = 1;
let enemySpeed = 2;

function drawPlayer() {
    ctx.fillStyle = player.color;
    ctx.fillRect(player.x, player.y, player.width, player.height);
}

function clearPlayer() {
    ctx.clearRect(player.x, player.y, player.width, player.height);
}

function movePlayer() {
    player.x += player.dx;

    if (player.x < 0) {
        player.x = 0;
    } else if (player.x + player.width > canvas.width) {
        player.x = canvas.width - player.width;
    }
}

function drawBullets() {
    bullets.forEach((bullet, index) => {
        ctx.fillStyle = '#ff0000';
        ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
        bullet.y -= bullet.speed;

        if (bullet.y + bullet.height < 0) {
            bullets.splice(index, 1);
        }
    });
}

function createEnemies() {
    for (let row = 0; row < enemyRows; row++) {
        for (let col = 0; col < enemyColumns; col++) {
            const enemy = {
                x: col * (enemyWidth + enemyPadding),
                y: row * (enemyHeight + enemyPadding),
                width: enemyWidth,
                height: enemyHeight,
                color: '#ff00ff'
            };
            enemies.push(enemy);
        }
    }
}

function drawEnemies() {
    enemies.forEach(enemy => {
        ctx.fillStyle = enemy.color;
        ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
    });
}

function moveEnemies() {
    let edge = false;
    enemies.forEach(enemy => {
        enemy.x += enemySpeed * enemyDirection;
        if (enemy.x + enemy.width > canvas.width || enemy.x < 0) {
            edge = true;
        }
    });

    if (edge) {
        enemyDirection *= -1;
        enemies.forEach(enemy => {
            enemy.y += enemyHeight;
        });
    }
}

function update() {
    clearPlayer();
    movePlayer();
    drawPlayer();
    drawBullets();
    drawEnemies();
    moveEnemies();
    requestAnimationFrame(update);
}

function shoot() {
    const bullet = {
        x: player.x + player.width / 2 - 5,
        y: player.y,
        width: 10,
        height: 20,
        speed: 10
    };
    bullets.push(bullet);
}

function keyDown(e) {
    if (e.key === 'ArrowRight') {
        player.dx = player.speed;
    } else if (e.key === 'ArrowLeft') {
        player.dx = -player.speed;
    } else if (e.key === ' ') {
        shoot();
    }
}

function keyUp(e) {
    if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        player.dx = 0;
    }
}

document.addEventListener('keydown', keyDown);
document.addEventListener('keyup', keyUp);

createEnemies();
update();