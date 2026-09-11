const loginForm =
    document.getElementById("login-form");

const loginMessage =
    document.getElementById("login-message");


loginForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        const email =
            document.getElementById(
                "email"
            ).value.trim();

        const password =
            document.getElementById(
                "password"
            ).value;

        loginMessage.textContent =
            "Signing in...";

        try {

            const response =
                await fetch(
                    "/api/auth/login",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type":
                                "application/json"
                        },
                        body: JSON.stringify({
                            email: email,
                            password: password
                        })
                    }
                );

            const data =
                await response.json();

            if (!response.ok) {
                loginMessage.textContent =
                    data.error ||
                    "Login failed.";

                return;
            }

            localStorage.setItem(
                "security_token",
                data.token
            );

            localStorage.setItem(
                "security_user",
                JSON.stringify(
                    data.user
                )
            );

            if (
                data.user.role ===
                "owner"
            ) {
                window.location.href =
                    "/owner";
            } else {
                window.location.href =
                    "/dashboard";
            }

        } catch (error) {

            loginMessage.textContent =
                "Server connection failed.";

        }
    }
);
