let hunger = 100;
let happiness = 100;
let cleanliness = 100;

const hungerDisplay = document.getElementById('hunger');
const happinessDisplay = document.getElementById('happiness');
const cleanlinessDisplay = document.getElementById('cleanliness');

document.getElementById('feed-btn').addEventListener('click', () => {
    hunger = Math.min(hunger + 10, 100);
    happiness = Math.min(happiness + 5, 100);
    updateStatus();
});

document.getElementById('play-btn').addEventListener('click', () => {
    happiness = Math.min(happiness + 10, 100);
    hunger = Math.max(hunger - 5, 0);
    updateStatus();
});

document.getElementById('clean-btn').addEventListener('click', () => {
    cleanliness = Math.min(cleanliness + 10, 100);
    happiness = Math.min(happiness + 5, 100);
    updateStatus();
});

function updateStatus() {
    hungerDisplay.textContent = hunger;
    happinessDisplay.textContent = happiness;
    cleanlinessDisplay.textContent = cleanliness;
}

setInterval(() => {
    hunger = Math.max(hunger - 1, 0);
    happiness = Math.max(happiness - 1, 0);
    cleanliness = Math.max(cleanliness - 1, 0);
    updateStatus();
}, 5000);