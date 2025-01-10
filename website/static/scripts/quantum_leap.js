function leapToDimension(dimension) {
    const resultDiv = document.getElementById('quantum-result');
    const dimensions = document.querySelectorAll('.dimension');

    dimensions.forEach(dim => dim.style.pointerEvents = 'none');

    setTimeout(() => {
        resultDiv.textContent = `Leaping to Dimension ${dimension}...`;
        setTimeout(() => {
            resultDiv.textContent = `You have successfully leaped to Dimension ${dimension}!`;
            dimensions.forEach(dim => dim.style.pointerEvents = 'auto');
        }, 2000);
    }, 1000);
}