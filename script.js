"use strict";

/*
 * Cybersecurity AI Platform
 * Core frontend controller
 *
 * این فایل فعلاً فقط رفتارهای پایه سایت را مدیریت می‌کند.
 * احراز هویت، پرداخت و اطلاعات حساس باید بعداً در Backend پیاده‌سازی شوند.
 */


/* =========================================
   APPLICATION STATE
========================================= */

const AppState = {
    initialized: false,
    user: null,
    plan: "free",
    authenticated: false
};


/* =========================================
   DOM HELPERS
========================================= */

function $(selector) {
    return document.querySelector(selector);
}

function $$(selector) {
    return document.querySelectorAll(selector);
}


/* =========================================
   NOTIFICATION SYSTEM
========================================= */

function showNotification(message, type = "info") {

    const existing = document.querySelector(".app-notification");

    if (existing) {
        existing.remove();
    }

    const notification = document.createElement("div");

    notification.className = "app-notification";

    notification.textContent = message;

    notification.style.position = "fixed";
    notification.style.bottom = "25px";
    notification.style.right = "25px";
    notification.style.zIndex = "99999";
    notification.style.maxWidth = "360px";
    notification.style.padding = "16px 20px";
    notification.style.borderRadius = "12px";
    notification.style.background = "#111";
    notification.style.color = "#fff";
    notification.style.border = "1px solid #333";
    notification.style.boxShadow = "0 15px 50px rgba(0,0,0,.45)";
    notification.style.fontSize = "14px";

    if (type === "success") {
        notification.style.borderColor = "#666";
    }

    if (type === "error") {
        notification.style.borderColor = "#999";
    }

    document.body.appendChild(notification);

    setTimeout(() => {

        notification.style.opacity = "0";
        notification.style.transform = "translateY(10px)";
        notification.style.transition = "0.3s";

        setTimeout(() => {
            notification.remove();
        }, 300);

    }, 3500);
}


/* =========================================
   SMOOTH NAVIGATION
========================================= */

function initializeNavigation() {

    const links = $$('a[href^="#"]');

    links.forEach(link => {

        link.addEventListener("click", function(event) {

            const targetId = this.getAttribute("href");

            if (!targetId || targetId === "#") {
                return;
            }

            const target = document.querySelector(targetId);

            if (!target) {
                return;
            }

            event.preventDefault();

            target.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        });

    });

}


/* =========================================
   PLAN BUTTONS
========================================= */

function initializePlanButtons() {

    const buttons = $$(".plan-card button");

    buttons.forEach(button => {

        button.addEventListener("click", function() {

            const card = this.closest(".plan-card");

            if (!card) {
                return;
            }

            const isPro = card.classList.contains("pro");

            if (isPro) {

                showNotification(
                    "Pro checkout will be connected to the secure payment system later.",
                    "info"
                );

                return;
            }

            showNotification(
                "Free plan selected.",
                "success"
            );

        });

    });

}


/* =========================================
   ACCOUNT ACTIONS
========================================= */

function initializeAccountButtons() {

    const accountLinks = $$(
        'a[href="#login"], a[href="#start"]'
    );

    accountLinks.forEach(link => {

        link.addEventListener("click", function(event) {

            const targetId = this.getAttribute("href");

            if (
                targetId === "#login" ||
                targetId === "#start"
            ) {

                event.preventDefault();

                showNotification(
                    "Account system will be connected in the next stage.",
                    "info"
                );

            }

        });

    });

}


/* =========================================
   SECURITY FEATURE INTERACTION
========================================= */

function initializeFeatureCards() {

    const cards = $$(".feature-card");

    cards.forEach(card => {

        card.addEventListener("click", function() {

            const titleElement = this.querySelector("h3");

            if (!titleElement) {
                return;
            }

            const featureName = titleElement.textContent.trim();

            showNotification(
                `${featureName} will be connected to the AI security engine.`,
                "info"
            );

        });

    });

}


/* =========================================
   SECURITY STATUS
========================================= */

const SecurityStatus = {

    level: "unknown",

    set(level) {

        const allowedLevels = [
            "unknown",
            "safe",
            "warning",
            "danger"
        ];

        if (!allowedLevels.includes(level)) {
            return;
        }

        this.level = level;

        document.body.dataset.securityStatus = level;

    },

    get() {
        return this.level;
    }

};


/* =========================================
   USER SESSION
========================================= */

const UserSession = {

    setUser(user) {

        if (!user || typeof user !== "object") {
            return;
        }

        AppState.user = user;
        AppState.authenticated = true;

        if (user.plan) {
            AppState.plan = user.plan;
        }

    },

    clear() {

        AppState.user = null;
        AppState.authenticated = false;
        AppState.plan = "free";

    },

    isAuthenticated() {
        return AppState.authenticated;
    },

    getPlan() {
        return AppState.plan;
    }

};


/* =========================================
   SAFE API HELPER
========================================= */

async function apiRequest(endpoint, options = {}) {

    const defaultOptions = {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    };

    const requestOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...(options.headers || {})
        }
    };

    try {

        const response = await fetch(
            endpoint,
            requestOptions
        );

        if (!response.ok) {

            throw new Error(
                `Request failed: ${response.status}`
            );

        }

        return await response.json();

    } catch (error) {

        console.error(
            "API request error:",
            error
        );

        throw error;
    }

}


/* =========================================
   APPLICATION INITIALIZATION
========================================= */

function initializeApplication() {

    if (AppState.initialized) {
        return;
    }

    initializeNavigation();
    initializePlanButtons();
    initializeAccountButtons();
    initializeFeatureCards();

    SecurityStatus.set("unknown");

    AppState.initialized = true;

    console.log(
        "Cybersecurity AI Platform initialized."
    );

}


/* =========================================
   START APPLICATION
========================================= */

if (
    document.readyState === "loading"
) {

    document.addEventListener(
        "DOMContentLoaded",
        initializeApplication
    );

} else {

    initializeApplication();

}
