// Add event listener to automatically scroll to the bottom of the chat messages
const chatMessages = document.querySelector('.chat-messages');
chatMessages.addEventListener('DOMSubtreeModified', () => {
    chatMessages.scrollTop = chatMessages.scrollHeight;
});

const hamburger = document.querySelector(".hamburger");
    const navLinks = document.querySelector(".nav-links");

    hamburger.addEventListener("click", () => {
        hamburger.classList.toggle("active");
        navLinks.classList.toggle("active");
});

const clearHistoryButton = document.getElementById('clear-history-button');
        clearHistoryButton.addEventListener('click', () => {
            // Send a request to clear the history.json file
            fetch('/clear_history', {
                method: 'POST'
            })
            .then(response => {
                if (response.ok) {
                    // If the history is cleared, reload the page
                    window.alert('History Cleared ✅');
                    location.reload();
                } else {
                    console.error('Error clearing history');
                }
            });
        });