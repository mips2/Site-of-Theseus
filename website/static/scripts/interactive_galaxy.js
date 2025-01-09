document.getElementById('explore-button').addEventListener('click', function() {
    const planets = document.querySelectorAll('.planet');
    planets.forEach(planet => {
        planet.style.animationDuration = `${Math.random() * 5 + 5}s`;
    });
    alert('Exploring the galaxy! Click on planets to learn more.');
});

document.querySelectorAll('.planet').forEach(planet => {
    planet.addEventListener('click', function() {
        alert(`You clicked on a planet! This planet is ${this.id}.`);
    });
});