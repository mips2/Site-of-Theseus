function exploreLocation(location) {
    const resultDiv = document.getElementById('exploration-result');
    const outcomes = {
        beach: "You found a treasure chest! 🏴‍☠️",
        jungle: "You discovered a hidden temple! 🛕",
        cave: "You encountered a mysterious creature! 🐉",
        volcano: "You found a rare gemstone! 💎"
    };

    resultDiv.innerHTML = outcomes[location] || "Nothing interesting here...";
}