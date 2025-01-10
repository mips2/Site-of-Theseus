function exploreLocation(location) {
    const resultDiv = document.getElementById('result');
    const locations = {
        beach: {
            message: "You found a treasure chest! 🏴‍☠️",
            reward: "100 gold coins"
        },
        jungle: {
            message: "You discovered a hidden temple! 🛕",
            reward: "Ancient artifact"
        },
        cave: {
            message: "You encountered a friendly dragon! 🐉",
            reward: "Dragon scale"
        },
        mountain: {
            message: "You reached the summit and found a magical crystal! 💎",
            reward: "Crystal of power"
        }
    };

    const result = locations[location];
    resultDiv.innerHTML = `
        <p>${result.message}</p>
        <p>Reward: ${result.reward}</p>
    `;
}