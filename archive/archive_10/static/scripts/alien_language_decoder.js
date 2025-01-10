document.getElementById('decode-button').addEventListener('click', function() {
    const alienText = document.getElementById('alien-text').value;
    const translatedText = document.getElementById('translated-text');
    
    const alienSymbols = {
        '👽': 'A',
        '🛸': 'B',
        '🌌': 'C',
        '🌟': 'D',
        '🌀': 'E'
    };

    let decodedMessage = '';
    for (let char of alienText) {
        decodedMessage += alienSymbols[char] || char;
    }

    translatedText.textContent = decodedMessage || 'No alien symbols detected!';
});

document.querySelectorAll('.symbol').forEach(symbol => {
    symbol.addEventListener('click', function() {
        const alienText = document.getElementById('alien-text');
        alienText.value += this.textContent;
    });
});