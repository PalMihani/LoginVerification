# LoginVerification (FastAPI + React)

This project is a full-stack WhatsApp-based OTP login and signup system. It uses **TextMeBot** to send OTPs to a user's personal WhatsApp number (no business account required), and stores verified users in a `Users.json` file on the backend.

---

## 🔧 Tech Stack

- ⚙️ **Backend**: Python, FastAPI
- 🎨 **Frontend**: React
- 💬 **WhatsApp API**: [TextMeBot](https://textmebot.com) (Free and personal-use friendly)
- 🗂️ **User Data**: Stored in `Users.json`

---

## ✨ Features

- OTP-based login via WhatsApp (TextMeBot API)
- 10-digit phone number validation
- Dropdown for country code selection
- Auto-signup for new users
- OTP verification and persistence
- Fully local frontend-backend integration (no deployment needed)

---

## 🚀 Setup Instructions

### 📦 Backend (FastAPI)

1. **Install dependencies**  
   Make sure you have Python 3.8+ installed.

   ```bash
   pip install fastapi uvicorn requests
