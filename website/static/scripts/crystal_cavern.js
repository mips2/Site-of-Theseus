document.addEventListener('DOMContentLoaded', () => {
    const crystals = document.querySelectorAll('.crystal');
    const treasureChest = document.querySelector('.treasure-chest');
    const winningCrystal = Math.floor(Math.random() * 9) + 1;

    crystals.forEach(crystal => {
        crystal.addEventListener('click', () => {
            const crystalValue = crystal.getAttribute('data-value');
            if (crystalValue == winningCrystal) {
                treasureChest.classList.remove('hidden');
                crystals.forEach(c => c.style.pointerEvents = 'none');
            } else {
                crystal.style.backgroundColor = '#ff0000';
                crystal.style.pointerEvents = 'none';
            }
        });
    });
});