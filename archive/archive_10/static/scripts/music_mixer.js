document.addEventListener('DOMContentLoaded', function() {
    const sounds = {
        kick: new Audio("{{ url_for('static', filename='sounds/kick.mp3') }}"),
        snare: new Audio("{{ url_for('static', filename='sounds/snare.mp3') }}"),
        hihat: new Audio("{{ url_for('static', filename='sounds/hihat.mp3') }}"),
        clap: new Audio("{{ url_for('static', filename='sounds/clap.mp3') }}"),
        cymbal: new Audio("{{ url_for('static', filename='sounds/cymbal.mp3') }}"),
        tom: new Audio("{{ url_for('static', filename='sounds/tom.mp3') }}")
    };

    document.querySelectorAll('.play-btn').forEach(button => {
        button.addEventListener('click', function() {
            const sound = this.getAttribute('data-sound');
            if (sounds[sound]) {
                sounds[sound].currentTime = 0;
                sounds[sound].play();
            }
        });
    });

    document.getElementById('play-all').addEventListener('click', function() {
        Object.values(sounds).forEach(sound => {
            sound.currentTime = 0;
            sound.play();
        });
    });

    document.getElementById('stop-all').addEventListener('click', function() {
        Object.values(sounds).forEach(sound => {
            sound.pause();
            sound.currentTime = 0;
        });
    });
});