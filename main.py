from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os, random, requests, json

# === TextMeBot API ===
TEXTMEBOT_API_KEY = "KEY"
USERS_FILE = "Users.json"

app = FastAPI()

# === Enable CORS for React frontend ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === OTP store (in-memory) ===
otp_store = {}

# === Load/Save Users JSON ===
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

user_store = load_users()

# === Pydantic models ===
class PhoneNumber(BaseModel):
    phone: str

class OtpInput(BaseModel):
    phone: str
    otp: str

class SignupInput(BaseModel):
    phone: str
    name: str
    email: str

# === Send OTP via TextMeBot ===
@app.post("/api/send_otp")
def send_otp(data: PhoneNumber):
    otp = str(random.randint(100000, 999999))
    otp_store[data.phone] = otp

    phone = data.phone.replace("+", "")
    url = f"https://api.textmebot.com/send.php?apikey={TEXTMEBOT_API_KEY}&phone=+{phone}&message=Your+OTP+is+{otp}"
    response = requests.get(url)

    print("=== TextMeBot DEBUG ===")
    print("URL:", url)
    print("Status Code:", response.status_code)
    print("Response:", response.text)
    print("=======================")

    if "Result: <b>Success!" in response.text:
        return {"message": "OTP sent via TextMeBot"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send OTP via TextMeBot")

# === Verify OTP ===
@app.post("/api/verify_otp")
def verify_otp(data: OtpInput):
    if otp_store.get(data.phone) != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    exists = data.phone in user_store
    return {"message": "OTP verified", "exists": exists}

# === Signup ===
@app.post("/api/signup")
def signup(data: SignupInput):
    if data.phone in user_store:
        raise HTTPException(status_code=400, detail="User already exists")
    user_store[data.phone] = {
        "name": data.name,
        "email": data.email
    }
    save_users(user_store)
    return {"message": "Signup successful"}

# === Serve React frontend ===
STATIC_DIR = "frontend-src/build/static"
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/{full_path:path}")
def serve_react(full_path: str):
    index_path = os.path.join("frontend-src", "build", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "React frontend not built yet"}
