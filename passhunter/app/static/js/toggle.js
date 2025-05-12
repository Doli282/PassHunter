/* 
Following code (file) was created by Cursor IDE.
AI model: Claude 3.7 Sonnet
prompt: Create a reusable JS function to toggle element visibility based on data attributes.
*/

// Remove no-js class if JS is enabled
document.documentElement.classList.remove('no-js');

document.addEventListener('DOMContentLoaded', () => {
    const toggleTriggers = document.querySelectorAll('[data-toggle-trigger]');

    toggleTriggers.forEach(trigger => {
        const targetSelector = trigger.getAttribute('data-toggle-target');
        const targetElement = document.querySelector(targetSelector);

        if (!targetElement) {
            console.warn(`Toggle target not found for selector: ${targetSelector}`);
            return;
        }

        // Hide the target element initially using JS
        targetElement.classList.add('hidden');

        // Ensure the target has an ID for aria-controls
        if (!targetElement.id) {
            console.warn(`Toggle target needs an ID for aria-controls: ${targetSelector}`);
        } else {
            trigger.setAttribute('aria-controls', targetElement.id);
        }

        // Store the original text only once during initialization
        const initialText = trigger.textContent.trim();
        trigger.setAttribute('data-original-text', initialText);
        trigger.setAttribute('aria-expanded', 'false');


        trigger.addEventListener('click', (event) => {
            event.preventDefault(); // Prevent default button behavior if it's a link etc.

            const isHidden = targetElement.classList.toggle('hidden');
            trigger.setAttribute('aria-expanded', !isHidden);

            // Change button text based on state, using the stored original text
            const currentToggleText = trigger.getAttribute('data-toggle-text');
            const originalText = trigger.getAttribute('data-original-text'); // Retrieve stored original

            if (currentToggleText && originalText) {
                trigger.textContent = isHidden ? originalText : currentToggleText;
            }
        });
    });
}); 