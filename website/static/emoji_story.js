document.addEventListener('DOMContentLoaded', function() {
    const emojiGrid = document.querySelector('.emoji-grid');
    const storyBox = document.querySelector('.story-box');
    const saveButton = document.querySelector('.save-story');

    emojiGrid.addEventListener('click', function(event) {
        if (event.target.tagName === 'SPAN') {
            storyBox.textContent += event.target.textContent;
        }
    });

    saveButton.addEventListener('click', function() {
        const story = storyBox.textContent;
        if (story.trim() === '') {
            alert('Please create a story before saving!');
            return;
        }
        alert('Story saved!');
        storyBox.textContent = '';
    });
});