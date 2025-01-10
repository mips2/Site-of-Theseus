document.getElementById('generate-art-btn').addEventListener('click', function() {
    const prompt = document.getElementById('prompt-input').value;
    if (prompt.trim() === "") {
        alert("Please enter a prompt!");
        return;
    }

    const artDisplay = document.getElementById('art-display');
    artDisplay.innerHTML = "Generating art...";

    // Simulate AI art generation with a delay
    setTimeout(() => {
        const randomArt = [
            "🎨✨", "🖼️🌈", "🌌🎆", "🦄🌠", "🌺🎨", "🌌🖌️", "🌠🖼️", "🌈✨"
        ];
        const randomIndex = Math.floor(Math.random() * randomArt.length);
        artDisplay.innerHTML = `<span style="font-size: 5rem;">${randomArt[randomIndex]}</span>`;
    }, 2000);
});