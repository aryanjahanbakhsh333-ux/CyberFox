const token =
    localStorage.getItem(
        "security_token"
    );

const message =
    document.getElementById(
        "dashboard-message"
    );


if (!token) {
    window.location.href = "/login";
}


async function apiGet(url) {

    const response =
        await fetch(
            url,
            {
                headers: {
                    "Authorization":
                        "Bearer " + token
                }
            }
        );

    return response.json();
}


async function loadDashboard() {

    try {

        const dashboard =
            await apiGet(
                "/api/dashboard/"
            );

        if (!dashboard.success) {
            window.location.href =
                "/login";

            return;
        }

        const user =
            dashboard.dashboard.user;

        document.getElementById(
            "welcome-title"
        ).textContent =
            "Welcome, " +
            user.email;

        document.getElementById(
            "welcome-text"
        ).textContent =
            "Your security dashboard is active.";

        document.getElementById(
            "user-plan"
        ).textContent =
            user.plan.toUpperCase();

        document.getElementById(
            "account-status"
        ).textContent =
            user.is_active
                ? "Active"
                : "Disabled";


        const score =
            await apiGet(
                "/api/security-score/"
            );

        if (score.success) {
            document.getElementById(
                "security-score"
            ).textContent =
                score.score + "/100";
        }


        const threats =
            await apiGet(
                "/api/threats/"
            );

        if (threats.success) {
            document.getElementById(
                "threat-count"
            ).textContent =
                threats.threats.length;
        }

    } catch (error) {

        message.textContent =
            "Unable to load dashboard.";

    }
}


document
    .getElementById("logout-button")
    .addEventListener(
        "click",
        async function () {

            await fetch(
                "/api/auth/logout",
                {
                    method: "POST",
                    headers: {
                        "Authorization":
                            "Bearer " + token
                    }
                }
            );

            localStorage.removeItem(
                "security_token"
            );

            localStorage.removeItem(
                "security_user"
            );

            window.location.href =
                "/login";
        }
    );


document
    .querySelectorAll(
        "[data-action]"
    )
    .forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    const action =
                        button.dataset.action;

                    message.textContent =
                        action +
                        " module is ready for connection.";

                }
            );
        }
    );


loadDashboard();
