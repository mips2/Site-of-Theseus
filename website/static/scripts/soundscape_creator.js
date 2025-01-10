document.addEventListener('DOMContentLoaded', () => {
    const sounds = {
        forest: new Audio('/static/sounds/forest.mp3'),
        ocean: new Audio('/static/sounds/ocean.mp3'),
        rain: new Audio('/static/sounds/rain.mp3'),
        city: new Audio('/static/sounds/city.mp3'),
        fire: new Audio('/static/sounds/fire.mp3'),
        birds: new Audio('/static/sounds/birds.mp3')
    };

    const soundElements = document.querySelectorAll('.sound');
    const playAllButton = document.getElementById('play-all');
    const stopAllButton = document.getElementById('stop-all');

    soundElements.forEach(soundElement => {
        soundElement.addEventListener('click', () => {
            const soundKey = soundElement.getAttribute('data-sound');
            if (sounds[soundKey].paused) {
                sounds[soundKey].play();
                soundElement.style.backgroundColor = 'rgba(255, 255, 255, 0.3)';
            } else {
                sounds[soundKey].pause();
                sounds[soundKey].currentTime = 0;
                soundElement.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
            }
        });
    });

    playAllButton.addEventListener('click', () => {
        Object.values(sounds).forEach(sound => {
            sound.play();
        });
        soundElements.forEach(soundElement => {
            soundElement.style.backgroundColor = 'rgba(255, 255, 255, 0.3)';
        });
    });

    stopAllButton.addEventListener('click', () => {
        Object.values(sounds).forEach(sound => {
            sound.pause();
            sound.currentTime = 0;
        });
        soundElements.forEach(soundElement => {
            soundElement.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
        });
    });
});