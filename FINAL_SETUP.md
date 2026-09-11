# Final Production Setup

## 1. Environment

Create a private `.env` file.

Never commit `.env` to Git.

Required production values:

SECRET_KEY=
DATABASE_URL=
REDIS_URL=

AI_API_KEY=
AI_BASE_URL=
AI_MODEL=

SMTP_HOST=
SMTP_PORT=
SMTP_USERNAME=
SMTP_PASSWORD=
EMAIL_SENDER=

PAYMENT_SECRET_KEY=
PAYMENT_WEBHOOK_SECRET=

OWNER_EMAIL=

## 2. Database

Use PostgreSQL in production.

Do not use the development SQLite database
for a public production deployment.

## 3. Redis

Use Redis for production rate limiting,
temporary verification data and distributed
application state.

## 4. Payments

Use Stripe Checkout.

Never store raw card numbers,
CVV values or payment credentials.

Pro access must be activated from a
verified payment webhook, not from a value
sent by the browser.

## 5. AI

Configure the AI provider through environment
variables.

Never expose AI_API_KEY to frontend JavaScript.

## 6. Email

Configure SMTP credentials only on the server.

Never expose SMTP credentials to the browser.

## 7. Autonomous Defense

Only execute actions against systems the
authenticated user is authorized to manage.

Destructive or unauthorized actions are not
part of the platform.

## 8. Deployment

Build:

docker compose -f docker-compose.production.yml build

Start:

docker compose -f docker-compose.production.yml up -d

## 9. Verification

Check:

/api/system/health

/api/system/readiness

/api/system/monitoring

Then run:

pytest
