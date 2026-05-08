# DriftDater

A full-stack dating web application built for INFO3180. Users can register, browse profiles, like or pass on others, chat with mutual matches, and manage their account — including optional two-factor authentication and dark mode.

## Team

| Name | Student ID | GitHub |
| [Khajeim Daily] | [620172076] | [@jeimtax](https://github.com/jeimtax) |
| [Randre Fearon] | [620167746] | [@drexify](https://github.com/drexify) |

---

## Tech Stack

**Backend**
- Python 3 / Flask 3
- PostgreSQL + SQLAlchemy + Flask-Migrate
- Flask-JWT-Extended (authentication)
- pyotp (TOTP two-factor authentication)

**Frontend**
- Vue 3 (Composition API, `<script setup>`)
- Vue Router 4
- Vite
- Bootstrap 5

---

## Features

### Mandatory
- User registration with profile photo upload
- Login with JWT-based session management
- Browse / Explore other users' public profiles
- Like or Pass on profiles
- View mutual matches
- Messaging between matched users
- Profile editing (bio, hobbies, location, relationship goal, visibility)
- Search & filter on the Explore page (name, location, age range, interests, sort order)
- Route guards (protected routes redirect to login; guests can't access auth-only pages)

### Optional
- **Dark Mode** — toggle persisted in `localStorage`, applied via `html.dark` CSS class
- **Two-Factor Authentication (TOTP)** — setup, enable, and disable from the Profile page using any authenticator app (Google Authenticator, Authy, etc.)

---

## Project Structure

```
info3180-datingapp/
├── app/
│   ├── __init__.py       # Flask app factory, extensions
│   ├── config.py         # Configuration (reads from .env)
│   ├── models.py         # SQLAlchemy models (User, Profile, Match, Message)
│   └── views.py          # All API routes (Blueprint: /api/v1)
├── migrations/           # Flask-Migrate migration files
├── static/
│   └── uploads/          # Uploaded profile pictures
├── src/                  # Vue 3 frontend
│   ├── assets/
│   ├── components/
│   │   ├── AppHeader.vue
│   │   ├── LoginForm.vue
│   │   ├── ProfileCard.vue
│   │   └── RegisterForm.vue
│   ├── composables/
│   │   └── useDarkMode.js
│   ├── router/
│   │   └── index.js
│   └── views/
│       ├── ExploreView.vue
│       ├── MatchesView.vue
│       ├── MessagesView.vue
│       └── ProfileView.vue
├── .env                  # Environment variables (not committed)
├── requirements.txt
└── package.json
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/info3180-datingapp.git
cd info3180-datingapp
```

### 2. Backend setup

```bash
# Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
DATABASE_URL=postgresql://username:password@localhost/driftdater
UPLOAD_FOLDER=./static/uploads
```

Run the database migrations:

```bash
flask db upgrade
```

Start the Flask development server:

```bash
flask run
```

The API will be available at `http://localhost:5000`.

### 3. Frontend setup

```bash
npm install
npm run dev
```

The Vue app will be available at `http://localhost:5173`.

---

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/v1/register` | No | Register a new user |
| POST | `/api/v1/auth/login` | No | Login (returns JWT or 2FA prompt) |
| POST | `/api/v1/auth/2fa/verify` | No | Complete 2FA login |
| GET | `/api/v1/auth/2fa/status` | JWT | Check if 2FA is enabled |
| POST | `/api/v1/auth/2fa/setup` | JWT | Generate TOTP secret + QR URI |
| POST | `/api/v1/auth/2fa/enable` | JWT | Confirm and enable 2FA |
| POST | `/api/v1/auth/2fa/disable` | JWT | Disable 2FA |
| GET | `/api/v1/explore` | JWT | Browse public profiles (with filters) |
| POST | `/api/v1/like` | JWT | Like or pass on a user |
| GET | `/api/v1/profile` | JWT | Get own profile |
| PUT | `/api/v1/profile` | JWT | Update own profile |
| GET | `/api/v1/matches` | JWT | List mutual matches |
| GET | `/api/v1/users/<id>` | JWT | Get another user's profile |
| GET | `/api/v1/conversations` | JWT | List message conversations |
| GET | `/api/v1/messages/<id>` | JWT | Get messages with a user |
| POST | `/api/v1/messages/<id>` | JWT | Send a message (matches only) |

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Flask session secret |
| `JWT_SECRET_KEY` | JWT signing secret |
| `DATABASE_URL` | PostgreSQL connection string |
| `UPLOAD_FOLDER` | Path for uploaded profile images |