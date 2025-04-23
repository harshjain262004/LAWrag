// This file contains the JavaScript code for the chat application. It handles user interactions, sends requests to the Flask backend, and updates the chat interface dynamically.

document.addEventListener("DOMContentLoaded", function() {
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const chatHistory = document.getElementById("chat-history");

    chatForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const query = userInput.value.trim();

        if (query) {
            appendMessage("You", query);
            userInput.value = "";

            fetch("/ask", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ question: query })
            })
            .then(response => response.json())
            .then(data => {
                appendMessage("Bot", data.answer);
            })
            .catch(error => {
                console.error("Error:", error);
                appendMessage("Bot", "Sorry, there was an error processing your request.");
            });
        }
    });

    function appendMessage(role, message) {
        const messageElement = document.createElement("div");
        messageElement.classList.add(role.toLowerCase());
        messageElement.innerHTML = `<strong>${role}:</strong> ${message}`;
        chatHistory.appendChild(messageElement);
        chatHistory.scrollTop = chatHistory.scrollHeight; // Scroll to the bottom
    }
});