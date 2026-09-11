const RecoveryTools = {

    async lockRecovery(lockType, provider) {
        const response = await fetch(
            "/api/recovery/lock",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization":
                        `Bearer ${localStorage.getItem("token") || ""}`
                },
                body: JSON.stringify({
                    lock_type: lockType,
                    provider: provider
                })
            }
        );

        return response.json();
    },

    async passwordRecovery(provider) {
        const response = await fetch(
            "/api/recovery/password",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization":
                        `Bearer ${localStorage.getItem("token") || ""}`
                },
                body: JSON.stringify({
                    provider: provider
                })
            }
        );

        return response.json();
    }
};
