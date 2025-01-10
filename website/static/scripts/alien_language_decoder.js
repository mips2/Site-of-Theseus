document.getElementById('decode-button').addEventListener('click', function() {
    const alienText = document.getElementById('alien-text').value;
    const translatedText = document.getElementById('translated-text');
    
    // Simple translation logic (replace with more complex logic if needed)
    const translationMap = {
        '🜁': 'A', '🜂': 'B', '🜃': 'C', '🜄': 'D', '🜅': 'E',
        '🜆': 'F', '🜇': 'G', '🜈': 'H', '🜉': 'I', '🜊': 'J'
    };

    let decodedText = '';
    for (let char of alienText) {
        decodedText += translationMap[char] || char;
    }

    translatedText.textContent = decodedText;
});

document.querySelectorAll('.symbol').forEach(symbol => {
    symbol.addEventListener('click', function() {
        const alienText = document.getElementById('alien-text');
        alienText.value += this.textContent;
    });
});