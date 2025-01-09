const planetData = {
    star1: { name: "Planet Zorak", description: "A mysterious planet with glowing blue oceans." },
    star2: { name: "Planet Luminos", description: "A bright planet with endless daylight." },
    star3: { name: "Planet Vortex", description: "A stormy planet with swirling red clouds." },
    star4: { name: "Planet Cryos", description: "A frozen planet with icy mountains." }
};

function explorePlanet(starId) {
    const planet = planetData[starId];
    const planetInfo = document.getElementById('planet-info');
    planetInfo.innerHTML = `
        <h2>${planet.name}</h2>
        <p>${planet.description}</p>
    `;
}