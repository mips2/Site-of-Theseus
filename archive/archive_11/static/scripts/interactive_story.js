const storyText = document.getElementById('story-text');
const choices = document.getElementById('choices');

const story = [
    {
        text: "Once upon a time, in a land far, far away...",
        options: [
            { text: "Explore the forest", next: 1 },
            { text: "Visit the castle", next: 2 },
            { text: "Talk to the villagers", next: 3 }
        ]
    },
    {
        text: "You venture into the dark forest. The trees are tall and the air is thick with mystery. What do you do?",
        options: [
            { text: "Climb a tree to get a better view", next: 4 },
            { text: "Follow a strange sound", next: 5 },
            { text: "Return to the village", next: 6 }
        ]
    },
    {
        text: "You approach the grand castle. The gates are open, but the courtyard is eerily silent. What's your next move?",
        options: [
            { text: "Enter the castle", next: 7 },
            { text: "Inspect the courtyard", next: 8 },
            { text: "Leave and head to the forest", next: 1 }
        ]
    },
    {
        text: "You talk to the villagers. They seem worried and whisper about a dragon in the nearby mountains. What do you do?",
        options: [
            { text: "Offer to help slay the dragon", next: 9 },
            { text: "Ask for more information", next: 10 },
            { text: "Ignore the rumors and go about your day", next: 11 }
        ]
    }
];

function chooseOption(optionIndex) {
    const currentStory = story[optionIndex];
    storyText.innerHTML = `<p>${currentStory.text}</p>`;
    choices.innerHTML = '';
    currentStory.options.forEach(option => {
        const button = document.createElement('button');
        button.textContent = option.text;
        button.onclick = () => chooseOption(option.next);
        choices.appendChild(button);
    });
}