document.addEventListener('DOMContentLoaded', () => {
    const player = document.getElementById('player');
    const opponent = document.getElementById('opponent');
    const raceButton = document.getElementById('race-button');
    const result = document.getElementById('result');
    let playerPosition = 0;
    let opponentPosition = 0;
    let raceInterval;

    raceButton.addEventListener('click', () => {
        if (!raceInterval) {
            raceInterval = setInterval(() => {
                playerPosition += Math.random() * 10;
                opponentPosition += Math.random() * 10;
                player.style.left = `${playerPosition}px`;
                opponent.style.left = `${opponentPosition}px`;

                if (playerPosition >= window.innerWidth - 50) {
                    clearInterval(raceInterval);
                    result.textContent = 'You Win! 🎉';
                } else if (opponentPosition >= window.innerWidth - 50) {
                    clearInterval(raceInterval);
                    result.textContent = 'Opponent Wins! 😢';
                }
            }, 50);
        }
    });
});