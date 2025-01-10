document.getElementById('send-button').addEventListener('click', function() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (message) {
        const messageDisplay = document.createElement('p');
        messageDisplay.textContent = `You: ${message}`;
        document.getElementById('hologram-message').appendChild(messageDisplay);
        input.value = '';

        // Simulate a hologram response
        setTimeout(() => {
            const hologramResponse = document.createElement('p');
            hologramResponse.textContent = `Hologram: ${message.split('').reverse().join('')}`;
            document.getElementById('hologram-message').appendChild(hologramResponse);
        }, 1000);
    }
});