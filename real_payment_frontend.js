async function upgradeToPro() {
    const token = localStorage.getItem("auth_token");

    if (!token) {
        alert("Please log in first.");
        return;
    }

    const response = await fetch(
        "/api/payment/checkout",
        {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        }
    );

    const data = await response.json();

    if (!response.ok || !data.success) {
        alert(
            data.error ||
            "Unable to start payment."
        );

        return;
    }

    window.location.href =
        data.checkout_url;
}


async function loadBillingStatus() {

    const token = localStorage.getItem(
        "auth_token"
    );

    if (!token) {
        return;
    }

    const response = await fetch(
        "/api/payment/status",
        {
            headers: {
                "Authorization":
                    `Bearer ${token}`
            }
        }
    );

    const data =
        await response.json();

    console.log(
        "Payment system:",
        data
    );
}


document.addEventListener(
    "DOMContentLoaded",
    loadBillingStatus
);
