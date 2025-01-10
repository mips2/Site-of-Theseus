document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star');
    const planetName = document.getElementById('planet-name');
    const planetDescription = document.getElementById('planet-description');

    const planetData = {
        mercury: {
            name: 'Mercury',
            description: 'Mercury is the smallest planet in our solar system and closest to the Sun. It has a rocky surface with many craters.'
        },
        venus: {
            name: 'Venus',
            description: 'Venus is the second planet from the Sun and is known for its thick atmosphere of carbon dioxide and sulfuric acid clouds.'
        },
        earth: {
            name: 'Earth',
            description: 'Earth is our home planet, the only place in the universe known to support life. It has a diverse environment and abundant water.'
        },
        mars: {
            name: 'Mars',
            description: 'Mars is the fourth planet from the Sun and is known as the Red Planet due to its reddish appearance. It has the largest volcano in the solar system.'
        },
        jupiter: {
            name: 'Jupiter',
            description: 'Jupiter is the largest planet in our solar system and is known for its Great Red Spot, a giant storm that has raged for centuries.'
        },
        saturn: {
            name: 'Saturn',
            description: 'Saturn is famous for its stunning ring system, made up of ice and rock particles. It is the sixth planet from the Sun.'
        },
        uranus: {
            name: 'Uranus',
            description: 'Uranus is the seventh planet from the Sun and is unique for its sideways rotation. It has a pale blue color due to methane in its atmosphere.'
        },
        neptune: {
            name: 'Neptune',
            description: 'Neptune is the eighth and farthest known planet from the Sun. It has the strongest winds in the solar system.'
        }
    };

    stars.forEach(star => {
        star.addEventListener('click', function() {
            const planet = this.getAttribute('data-planet');
            planetName.textContent = planetData[planet].name;
            planetDescription.textContent = planetData[planet].description;
        });
    });
});