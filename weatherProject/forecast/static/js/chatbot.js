document.addEventListener("DOMContentLoaded", () => {

    const sendBtn = document.getElementById("sendBtn");
    const input = document.getElementById("userMessage");
    const chatBox = document.getElementById("chat-box");

    if (!sendBtn || !input || !chatBox) {
        console.error("Chatbot elements not found.");
        return;
    }

    function addMessage(message, sender) {

        const div = document.createElement("div");

        div.className = sender;

        // Safer than innerHTML
        div.textContent = message;

        chatBox.appendChild(div);

        chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function sendMessage() {

        const message = input.value.trim();

        if (message === "") return;

        // Show user message
        addMessage(message, "user-message");

        input.value = "";

        // Show temporary message
        addMessage("🌤️ I'm thinking...", "bot-message");

        try {

            const response = await fetch("/ai-chat/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },
                body: JSON.stringify({
                    message: message,

                    weather: {
                        description:
                            document.querySelector(".condition")?.innerText || "",

                        temp:
                            parseInt(
                                document.querySelector(".hero-temp")?.innerText
                            ) || 0,

                        humidity:
                            parseInt(
                                document.querySelector(
                                    ".mini-grid div:nth-child(2) span"
                                )?.innerText
                            ) || 0,

                        wind:
                            parseInt(
                                document.querySelector(
                                    ".mini-grid div:nth-child(4) span"
                                )?.innerText
                            ) || 0
                    }
                })
            });

            if (!response.ok) {
                throw new Error("Server error: " + response.status);
            }

            const data = await response.json();

            // Remove "I'm thinking..."
            const messages = chatBox.querySelectorAll(".bot-message");

            if (messages.length > 0) {
                messages[messages.length - 1].remove();
            }

            // Show actual response
            addMessage(data.reply, "bot-message");

        } catch (error) {

            console.error("Chatbot error:", error);

            const messages = chatBox.querySelectorAll(".bot-message");

            if (messages.length > 0) {
                messages[messages.length - 1].remove();
            }

            addMessage(
                "❌ Sorry, I couldn't connect to the chatbot.",
                "bot-message"
            );
        }
    }

    // Send button
    sendBtn.addEventListener("click", sendMessage);

    // Press Enter to send
    input.addEventListener("keypress", (event) => {

        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }

    });

    function getCSRFToken() {

        const cookie = document.cookie
            .split("; ")
            .find(row => row.startsWith("csrftoken="));

        if (cookie) {
            return decodeURIComponent(cookie.split("=")[1]);
        }

        // Fallback to hidden Django CSRF input
        const csrfInput =
            document.querySelector("[name=csrfmiddlewaretoken]");

        return csrfInput ? csrfInput.value : "";
    }

});