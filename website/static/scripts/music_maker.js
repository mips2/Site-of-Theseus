const keys = document.querySelectorAll('.key');
const recordBtn = document.getElementById('record-btn');
const playBtn = document.getElementById('play-btn');
const clearBtn = document.getElementById('clear-btn');

let recordedNotes = [];
let isRecording = false;

keys.forEach(key => {
    key.addEventListener('click', () => {
        const note = key.getAttribute('data-note');
        playNote(note);
        if (isRecording) {
            recordedNotes.push(note);
        }
    });
});

recordBtn.addEventListener('click', () => {
    isRecording = !isRecording;
    recordBtn.textContent = isRecording ? '⏹ Stop Recording' : '🎤 Record';
    if (!isRecording) {
        alert('Recording stopped!');
    }
});

playBtn.addEventListener('click', () => {
    if (recordedNotes.length === 0) {
        alert('No notes recorded!');
        return;
    }
    recordedNotes.forEach((note, index) => {
        setTimeout(() => playNote(note), index * 500);
    });
});

clearBtn.addEventListener('click', () => {
    recordedNotes = [];
    alert('Recording cleared!');
});

function playNote(note) {
    const audio = new Audio(`/static/sounds/${note}.mp3`);
    audio.play();
}