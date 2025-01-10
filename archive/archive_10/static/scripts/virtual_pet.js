let hunger = 100;
let happiness = 100;
let cleanliness = 100;

const hungerDisplay = document.getElementById('hunger');
const happinessDisplay = document.getElementById('happiness');
const cleanlinessDisplay = document.getElementById('cleanliness');

const feedBtn = document.getElementById('feed-btn');
const playBtn = document.getElementById('play-btn');
const cleanBtn = document.getElementById('clean-btn');

feedBtn.addEventListener('click', () => {
    hunger = Math.min(hunger + 10, 100);
    happiness = Math.min(happiness + 5, 100);
    updateStats();
});

playBtn.addEventListener('click', () => {
    happiness = Math.min(happiness + 10, 100);
    hunger = Math.max(hunger - 5, 0);
    updateStats();
});

cleanBtn.addEventListener('click', () => {
    cleanliness = Math.min(cleanliness + 10, 100);
    happiness = Math.min(happiness + 5, 100);
    updateStats();
});

function updateStats() {
    hungerDisplay.textContent = hunger;
    happinessDisplay.textContent = happiness;
    cleanlinessDisplay.textContent = cleanliness;
    checkPetStatus();
}

function checkPetStatus() {
    if (hunger <= 0 || happiness <= 0 || cleanliness <= 0) {
        alert('Your pet is not feeling well! Take better care of it!');
    }
}

setInterval(() => {
    hunger = Math.max(hunger - 1, 0);
    happiness = Math.max(happiness - 1, 0);
    cleanliness = Math.max(cleanliness - 1, 0);
    updateStats();
}, 5000);