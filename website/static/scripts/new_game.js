document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star');
    const planetName = document.getElementById('planet-name');
    const planetDescription = document.getElementById('planet-description');

    const planets = {
        1: { name: "Aurora Prime", description: "A planet with shimmering auroras and icy landscapes." },
        2: { name: "Crimson Dusk", description: "A red desert planet with ancient ruins." },
        3: { name: "Emerald Haven", description: "A lush green planet teeming with life." },
        4: { name: "Obsidian Void", description: "A dark planet with mysterious black crystals." },
        5: { name: "Celestial Mirage", description: "A planet that appears and disappears in the void." }
    };

    stars.forEach(star => {
        star.addEventListener('click', function() {
            const planetId = this.getAttribute('data-planet');
            const planet = planets[planetId];
            planetName.textContent = planet.name;
            planetDescription.textContent = planet.description;
        });
    });
});