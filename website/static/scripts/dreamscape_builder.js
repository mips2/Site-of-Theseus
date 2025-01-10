document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('dreamscape-canvas');
    const tools = document.querySelectorAll('.tool');
    let selectedElement = null;

    tools.forEach(tool => {
        tool.addEventListener('click', function() {
            selectedElement = this.getAttribute('data-type');
        });
    });

    canvas.addEventListener('click', function(event) {
        if (selectedElement) {
            const element = document.createElement('div');
            element.className = 'dream-element';
            element.textContent = getEmoji(selectedElement);
            element.style.position = 'absolute';
            element.style.left = `${event.offsetX - 25}px`;
            element.style.top = `${event.offsetY - 25}px`;
            element.style.fontSize = '50px';
            element.style.cursor = 'pointer';
            canvas.appendChild(element);

            element.addEventListener('click', function(e) {
                e.stopPropagation();
                canvas.removeChild(element);
            });
        }
    });

    document.getElementById('save-dreamscape').addEventListener('click', function() {
        alert('Dreamscape saved! (This is a demo, no actual saving occurs.)');
    });

    function getEmoji(type) {
        switch (type) {
            case 'mountain': return '🏔️';
            case 'tree': return '🌳';
            case 'river': return '🌊';
            case 'castle': return '🏰';
            case 'cloud': return '☁️';
            default: return '';
        }
    }
});