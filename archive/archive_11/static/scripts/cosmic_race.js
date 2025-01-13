document.addEventListener('DOMContentLoaded', () => {
    const playerSpaceship = document.getElementById('player-spaceship');
    const aiSpaceship = document.getElementById('ai-spaceship');
    const raceButton = document.getElementById('race-button');
    const result = document.getElementById('result');
    const trackWidth = document.querySelector('.race-track').clientWidth - 50;
    let playerPosition = 0;
    let aiPosition = 0;

    raceButton.addEventListener('click', () => {
        playerPosition += Math.random() * 20;
        playerSpaceship.style.left = `${Math.min(playerPosition, trackWidth)}px`;

        aiPosition += Math.random() * 15;
        aiSpaceship.style.left = `${Math.min(aiPosition, trackWidth)}px`;

        if (playerPosition >= trackWidth && aiPosition >= trackWidth) {
            result.textContent = "It's a tie!";
            resetRace();
        } else if (playerPosition >= trackWidth) {
            result.textContent = "You win!";
            resetRace();
        } else if (aiPosition >= trackWidth) {
            result.textContent = "AI wins!";
            resetRace();
        }
    });

    function resetRace() {
        playerPosition = 0;
        aiPosition = 0;
        playerSpaceship.style.left = '0';
        aiSpaceship.style.left = '0';
    }
});