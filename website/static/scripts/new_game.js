document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star');
    const starDetails = document.getElementById('star-details');

    stars.forEach(star => {
        star.addEventListener('click', function() {
            const starId = this.getAttribute('data-star');
            const starInfo = getStarInfo(starId);
            starDetails.textContent = starInfo;
        });
    });

    function getStarInfo(starId) {
        const starData = {
            1: "Star Alpha: A young star with a vibrant blue hue.",
            2: "Star Beta: A red giant nearing the end of its life cycle.",
            3: "Star Gamma: A binary star system with two stars orbiting each other.",
            4: "Star Delta: A neutron star with an incredibly dense core."
        };
        return starData[starId] || "Unknown star.";
    }
});