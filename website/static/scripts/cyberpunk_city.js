function exploreDistrict(districtId) {
    const districtInfo = document.getElementById('district-info');
    let infoText = '';

    switch (districtId) {
        case 'downtown':
            infoText = 'You find yourself in the bustling heart of Cyberpunk City. Neon lights flash all around you, and the sound of hovercars fills the air.';
            break;
        case 'industrial':
            infoText = 'The Industrial Zone is a maze of factories and warehouses. The air is thick with smoke, and the hum of machinery is constant.';
            break;
        case 'residential':
            infoText = 'The Residential Area is quieter, with rows of high-rise apartments. You can see people going about their daily lives, oblivious to the chaos of the city.';
            break;
        default:
            infoText = 'You have entered an unknown district. Be cautious.';
    }

    districtInfo.innerHTML = `<p>${infoText}</p>`;
}