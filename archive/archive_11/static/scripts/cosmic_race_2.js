document.addEventListener('DOMContentLoaded', () => {
    const player1 = document.getElementById('player1');
    const player2 = document.getElementById('player2');
    const startRaceButton = document.getElementById('start-race');
    const resetRaceButton = document.getElementById('reset-race');
    const score1 = document.getElementById('score1');
    const score2 = document.getElementById('score2');

    let raceInterval;
    let player1Position = 10;
    let player2Position = 10;
    let player1Score = 0;
    let player2Score = 0;

    startRaceButton.addEventListener('click', () => {
        clearInterval(raceInterval);
        raceInterval = setInterval(() => {
            player1Position += Math.random() * 5;
            player2Position += Math.random() * 5;

            player1.style.left = `${player1Position}%`;
            player2.style.left = `${player2Position}%`;

            if (player1Position >= 90) {
                clearInterval(raceInterval);
                player1Score++;
                score1.textContent = player1Score;
                alert('Player 1 Wins!');
            } else if (player2Position >= 90) {
                clearInterval(raceInterval);
                player2Score++;
                score2.textContent = player2Score;
                alert('Player 2 Wins!');
            }
        }, 50);
    });

    resetRaceButton.addEventListener('click', () => {
        clearInterval(raceInterval);
        player1Position = 10;
        player2Position = 10;
        player1.style.left = `${player1Position}%`;
        player2.style.left = `${player2Position}%`;
    });
});