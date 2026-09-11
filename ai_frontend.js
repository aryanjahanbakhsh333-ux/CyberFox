const AISecurity = {
    async analyze(target, findings, context = {}) {
        const response = await fetch(
            "/api/ai-security/analyze",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization":
                        `Bearer ${localStorage.getItem("token") || ""}`
                },
                body: JSON.stringify({
                    target,
                    findings,
                    context
                })
            }
        );

        return response.json();
    },

    async chat(message, conversation = []) {
        const response = await fetch(
            "/api/ai-chat/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization":
                        `Bearer ${localStorage.getItem("token") || ""}`
                },
                body: JSON.stringify({
                    message,
                    conversation
                })
            }
        );

        return response.json();
    }
};
