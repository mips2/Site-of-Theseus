document.getElementById('travel-button').addEventListener('click', function() {
    const year = document.getElementById('year-input').value;
    if (year) {
        fetch(`/api/historical-events?year=${year}`)
            .then(response => response.json())
            .then(data => {
                const resultDiv = document.getElementById('time-travel-result');
                if (data.events.length > 0) {
                    resultDiv.innerHTML = `<h2>Events in ${year}:</h2><ul>${data.events.map(event => `<li>${event}</li>`).join('')}</ul>`;
                } else {
                    resultDiv.innerHTML = `<p>No significant events found for ${year}. Try another year!</p>`;
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
});