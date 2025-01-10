document.getElementById('time-capsule-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const message = document.getElementById('message').value;
    const revealDate = new Date(document.getElementById('reveal-date').value);
    const now = new Date();
    
    if (revealDate <= now) {
        alert('Please select a future date!');
        return;
    }
    
    const timeDiff = revealDate - now;
    const days = Math.floor(timeDiff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((timeDiff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeDiff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeDiff % (1000 * 60)) / 1000);
    
    document.getElementById('countdown').innerHTML = `Your message will be revealed in: ${days}d ${hours}h ${minutes}m ${seconds}s`;
    
    setInterval(() => {
        const now = new Date();
        const timeDiff = revealDate - now;
        const days = Math.floor(timeDiff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((timeDiff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((timeDiff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeDiff % (1000 * 60)) / 1000);
        
        document.getElementById('countdown').innerHTML = `Your message will be revealed in: ${days}d ${hours}h ${minutes}m ${seconds}s`;
        
        if (timeDiff <= 0) {
            clearInterval();
            document.getElementById('countdown').innerHTML = `Your message is revealed: ${message}`;
        }
    }, 1000);
});