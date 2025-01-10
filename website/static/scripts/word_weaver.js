document.getElementById('addWordBtn').addEventListener('click', function() {
    const wordInput = document.getElementById('wordInput');
    const storyDisplay = document.getElementById('storyDisplay');

    if (wordInput.value.trim() !== '') {
        const wordSpan = document.createElement('span');
        wordSpan.textContent = wordInput.value + ' ';
        wordSpan.style.color = getRandomColor();
        storyDisplay.appendChild(wordSpan);
        wordInput.value = '';
    }
});

function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}