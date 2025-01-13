document.getElementById('submit-action').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() === '') return;

    const storyDisplay = document.getElementById('story-display');
    const userAction = document.createElement('p');
    userAction.textContent = `You: ${userInput}`;
    storyDisplay.appendChild(userAction);

    fetch('/ai-dungeon-master-response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        const aiResponse = document.createElement('p');
        aiResponse.textContent = `AI Dungeon Master: ${data.response}`;
        storyDisplay.appendChild(aiResponse);
        storyDisplay.scrollTop = storyDisplay.scrollHeight;
    })
    .catch(error => console.error('Error:', error));

    document.getElementById('user-input').value = '';
});