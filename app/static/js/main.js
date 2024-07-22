document.addEventListener('DOMContentLoaded', function() {
    // Apply animations to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseover', () => {
            button.classList.add('button-anim');
        });
        button.addEventListener('mouseout', () => {
            button.classList.remove('button-anim');
        });
    });

    // Toggle for light and dark mode
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('change', () => {
            const theme = document.documentElement;
            if (themeToggle.checked) {
                theme.setAttribute('data-theme', 'dark');
            } else {
                theme.setAttribute('data-theme', 'light');
            }
        });
    }
});


// A function to dynamically adjust styles or respond to events
function updateStylesOnEvent() {
    const specialElements = document.querySelectorAll('.special-class');
    specialElements.forEach(element => {
        element.style.color = 'red'; // Example of dynamic styling
    });
}

// Function to ensure elements are ready before executing animations
function safeAddClass(element, className) {
    if (element) {
        element.classList.add(className);
    }
}

// Error handling example
function handleError() {
    console.error('An error occurred with the interaction.');
}
