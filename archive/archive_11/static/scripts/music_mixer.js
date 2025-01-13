document.addEventListener('DOMContentLoaded', function() {
    const tracks = document.querySelectorAll('.track');

    tracks.forEach(track => {
        const playBtn = track.querySelector('.play-btn');
        const audio = track.querySelector('audio');
        const volumeSlider = track.querySelector('.volume');

        playBtn.addEventListener('click', () => {
            if (audio.paused) {
                audio.play();
                playBtn.textContent = '⏸️';
            } else {
                audio.pause();
                playBtn.textContent = '▶️';
            }
        });

        volumeSlider.addEventListener('input', () => {
            audio.volume = volumeSlider.value / 100;
        });
    });

    document.getElementById('play-all').addEventListener('click', () => {
        tracks.forEach(track => {
            const audio = track.querySelector('audio');
            const playBtn = track.querySelector('.play-btn');
            audio.play();
            playBtn.textContent = '⏸️';
        });
    });

    document.getElementById('stop-all').addEventListener('click', () => {
        tracks.forEach(track => {
            const audio = track.querySelector('audio');
            const playBtn = track.querySelector('.play-btn');
            audio.pause();
            audio.currentTime = 0;
            playBtn.textContent = '▶️';
        });
    });
});