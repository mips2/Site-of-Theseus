function mixEmojis() {
    const emoji1 = document.getElementById('emoji1').value;
    const emoji2 = document.getElementById('emoji2').value;
    const mixedEmoji = document.getElementById('mixedEmoji');

    // Simple emoji mixing logic
    const mixedResult = emoji1 + emoji2;
    mixedEmoji.textContent = mixedResult;
}