const canvas = document.getElementById('gravityCanvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth * 0.8;
canvas.height = window.innerHeight * 0.8;

let planets = [];
let mouse = { x: 0, y: 0, isDown: false };

class Planet {
    constructor(x, y, mass) {
        this.x = x;
        this.y = y;
        this.mass = mass;
        this.radius = Math.sqrt(mass) * 2;
        this.vx = 0;
        this.vy = 0;
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = 'white';
        ctx.fill();
        ctx.closePath();
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;
    }
}

function applyGravity() {
    for (let i = 0; i < planets.length; i++) {
        for (let j = 0; j < planets.length; j++) {
            if (i !== j) {
                const dx = planets[j].x - planets[i].x;
                const dy = planets[j].y - planets[i].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                const force = (planets[j].mass * planets[i].mass) / (distance * distance);
                const angle = Math.atan2(dy, dx);
                planets[i].vx += (force * Math.cos(angle)) / planets[i].mass * 0.1;
                planets[i].vy += (force * Math.sin(angle)) / planets[i].mass * 0.1;
            }
        }
    }
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    applyGravity();
    planets.forEach(planet => {
        planet.update();
        planet.draw();
    });
    requestAnimationFrame(animate);
}

canvas.addEventListener('mousedown', (e) => {
    mouse.isDown = true;
    mouse.x = e.offsetX;
    mouse.y = e.offsetY;
});

canvas.addEventListener('mousemove', (e) => {
    if (mouse.isDown) {
        mouse.x = e.offsetX;
        mouse.y = e.offsetY;
    }
});

canvas.addEventListener('mouseup', () => {
    if (mouse.isDown) {
        planets.push(new Planet(mouse.x, mouse.y, Math.random() * 50 + 10));
        mouse.isDown = false;
    }
});

animate();