function choosePath(path) {
    const storyText = document.getElementById('story-text');
    const choices = document.getElementById('choices');

    if (path === 'forest') {
        storyText.innerHTML = `
            <p>You step into the dark forest. The trees are tall and the air is thick with mist. Suddenly, you hear a rustling in the bushes. What do you do?</p>
        `;
        choices.innerHTML = `
            <button onclick="choosePath('investigate')">Investigate the Noise</button>
            <button onclick="choosePath('run')">Run Away</button>
        `;
    } else if (path === 'meadow') {
        storyText.innerHTML = `
            <p>You walk into the sunny meadow. The grass is soft under your feet, and the air smells of wildflowers. You see a small cottage in the distance. What do you do?</p>
        `;
        choices.innerHTML = `
            <button onclick="choosePath('cottage')">Approach the Cottage</button>
            <button onclick="choosePath('explore')">Explore the Meadow</button>
        `;
    } else if (path === 'investigate') {
        storyText.innerHTML = `
            <p>You cautiously approach the rustling bushes. A small, friendly rabbit hops out and looks up at you. It seems to want you to follow it.</p>
        `;
        choices.innerHTML = `
            <button onclick="choosePath('follow')">Follow the Rabbit</button>
            <button onclick="choosePath('ignore')">Ignore the Rabbit</button>
        `;
    } else if (path === 'run') {
        storyText.innerHTML = `
            <p>You turn and run as fast as you can. The forest seems to close in around you, and you soon find yourself lost. You stumble upon a hidden cave.</p>
        `;
        choices.innerHTML = `
            <button onclick="choosePath('enterCave')">Enter the Cave</button>
            <button onclick="choosePath('keepRunning')">Keep Running</button>
        `;
    } else if (path === 'cottage') {
        storyText.innerHTML = `
            <p>You approach the cottage and knock on the door. An old woman answers and invites you in for tea. She seems to know a lot about the area.</p>
        `;
        choices.innerHTML = `
            <button onclick="choosePath('askAboutForest')">Ask About the Forest</button>
            <button onclick="choosePath('thankHer')">Thank Her and Leave</button>
        `;
    } else if (path === 'explore') {
        storyText.innerHTML = `
            <p>You spend hours exploring the meadow, discovering hidden streams and colorful flowers. As the sun sets, you find a perfect spot to rest.</p>
        `;
        choices.innerHTML = `
            <button onclick="choosePath('rest')">Rest for the Night</button>
            <button onclick="choosePath('return')">Return to the Crossroads</button>
        `;
    } else if (path === 'follow') {
        storyText.innerHTML = `
            <p>You follow the rabbit deep into the forest. It leads you to a hidden glade filled with glowing mushrooms and a sparkling pond. You feel a sense of peace.</p>
        `;
        choices.innerHTML = `
            <button onclick="choosePath('stay')">Stay in the Glade</button>
            <button onclick="choosePath('return')">Return to the Crossroads</button>
        `;
    } else if (path === 'ignore') {
        storyText.innerHTML = `
            <p>You ignore the rabbit and continue on your way. The forest grows darker and more ominous. You soon realize you are being watched.</p>
        `;
        choices.innerHTML = `
            <button onclick="choosePath('confront')">Confront the Watcher</button>
            <button onclick="choosePath('hide')">Hide and Wait</button>
        `;
    } else if (path === 'enterCave') {
        storyText.innerHTML = `
            <p>You enter the cave and find a treasure chest filled with gold and jewels. You have found your fortune!</p>
        `;
        choices.innerHTML = `
            <button onclick="choosePath('end')">Take the Treasure</button>
        `;
    } else if (path === 'keepRunning') {
        storyText.innerHTML = `
            <p>You keep running and eventually find your way out of the forest. You emerge into a new land, full of possibilities.</p>
        `;
        choices.innerHTML = `
            <button onclick="choosePath('end')">Continue Your Journey</button>
        `;
    } else if (path === 'askAboutForest') {
        storyText.innerHTML = `
            <p>The old woman tells you that the forest is enchanted and holds many secrets. She gives you a map to help you navigate it.</p>
        `;
        choices.innerHTML = `
            <button onclick="choosePath('thankHer')">Thank Her and Leave</button>
        `;
    } else if (path === 'thankHer') {
        storyText.innerHTML = `
            <p>You thank the old woman and leave the cottage. You feel more prepared for your journey ahead.</p>
        `;
        choices.innerHTML = `
            <button onclick="choosePath('return')">Return to the Crossroads</button>
        `;
    } else if (path === 'rest') {
        storyText.innerHTML = `
            <p>You rest for the night under the stars. The next morning, you wake up feeling refreshed and ready to continue your adventure.</p>
        `;
        choices.innerHTML = `
            <button onclick="choosePath('return')">Return to the Crossroads</button>
        `;
    } else if (path === 'confront') {
        storyText.innerHTML = `
            <p>You confront the watcher, who turns out to be a friendly forest guardian. They offer to guide you through the forest.</p>
        `;
        choices.innerHTML = `
            <button onclick="choosePath('followGuardian')">Follow the Guardian</button>
            <button onclick="choosePath('decline')">Decline and Go Your Own Way</button>
        `;
    } else if (path === 'hide') {
        storyText.innerHTML = `
            <p>You hide and wait, but the watcher finds you. It turns out to be a mischievous sprite who offers you a magical gift.</p>
        `;
        choices.innerHTML = `
            <button onclick="choosePath('acceptGift')">Accept the Gift</button>
            <button onclick="choosePath('decline')">Decline the Gift</button>
        `;
    } else if (path === 'followGuardian') {
        storyText.innerHTML = `
            <p>You follow the guardian through the forest, learning about its secrets and history. You feel a deep connection to the land.</p>
        `;
        choices.innerHTML = `
            <button onclick="choosePath('end')">Continue Your Journey</button>
        `;
    } else if (path === 'decline') {
        storyText.innerHTML = `
            <p>You decline the offer and continue on your own path. The forest seems to respect your independence, and you find your way out safely.</p>
        `;
        choices.innerHTML = `
            <button onclick="choosePath('end')">Continue Your Journey</button>
        `;
    } else if (path === 'acceptGift') {
        storyText.innerHTML = `
            <p>You accept the magical gift, which grants you the ability to communicate with animals. You use this power to make new friends in the forest.</p>
        `;
        choices.innerHTML = `
            <button onclick="choosePath('end')">Continue Your Journey</button>
        `;
    } else if (path === 'end') {
        storyText.innerHTML = `
            <p>Your adventure comes to an end, but the memories will stay with you forever. Thank you for playing!</p>
        `;
        choices.innerHTML = `
            <button onclick="location.reload()">Play Again</button>
        `;
    }
}