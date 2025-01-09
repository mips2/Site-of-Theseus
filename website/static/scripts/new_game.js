function explorePlanet(starId) {
    const planets = {
        star1: { name: "Planet Zorblax", description: "A mysterious planet with glowing blue oceans." },
        star2: { name: "Planet Luminos", description: "A bright planet with endless daylight." },
        star3: { name: "Planet Cryos", description: "A frozen world with icy mountains." },
        star4: { name: "Planet Pyros", description: "A fiery planet with active volcanoes." }
    };

    const planet = planets[starId];
    const planetInfo = document.getElementById('planet-info');
    planetInfo.innerHTML = `<h2>${planet.name}</h2><p>${planet.description}</p>`;
}