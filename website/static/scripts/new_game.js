function explorePlanet(starId) {
    const planets = {
        star1: { name: "Planet Zorblax", description: "A mysterious planet with glowing blue oceans." },
        star2: { name: "Planet Quixar", description: "A rocky planet with towering crystal mountains." },
        star3: { name: "Planet Lumina", description: "A luminous planet with floating islands." },
        star4: { name: "Planet Vortex", description: "A swirling planet with endless storms." }
    };

    const planet = planets[starId];
    const planetInfo = document.getElementById('planet-info');
    planetInfo.innerHTML = `<h2>${planet.name}</h2><p>${planet.description}</p>`;
}