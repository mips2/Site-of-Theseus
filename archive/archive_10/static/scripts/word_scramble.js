const words = ['PYTHON', 'JAVASCRIPT', 'FLASK', 'REACT', 'HTML', 'CSS', 'NODEJS', 'DATABASE', 'API', 'FRAMEWORK'];
let currentWord = '';
let scrambledWord = '';
let score = 0;

function scrambleWord(word) {
    return word.split('').sort(() => Math.random() - 0.5).join('');
}

function newWord() {
    currentWord = words[Math.floor(Math.random() * words.length)];
    scrambledWord = scrambleWord(currentWord);
    document.getElementById('scrambled-word').textContent = scrambledWord;
    document.getElementById('user-input').value = '';
    document.getElementById('result').textContent = '';
}

function checkAnswer() {
    const userInput = document.getElementById('user-input').value.toUpperCase();
    if (userInput === currentWord) {
        document.getElementById('result').textContent = 'Correct!';
        score++;
        document.getElementById('score').textContent = score;
        newWord();
    } else {
        document.getElementById('result').textContent = 'Incorrect! Try again.';
    }
}

document.getElementById('submit-btn').addEventListener('click', checkAnswer);

newWord();