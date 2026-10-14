import hashlib
import secrets
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field

app = FastAPI(title="Auth API")

users = {}      # username -> {"salt": bytes, "hash": str}
tokens = {}     # token -> username
failed = {}     # username -> failed login count
MAX_FAILS = 6


class RegisterIn(BaseModel):
    username: str = Field(min_length=3, max_length=20, pattern=r"^[A-Za-z0-9_]+$")
    password: str = Field(min_length=8, max_length=64)


class LoginIn(BaseModel):
    username: str
    password: str


def hash_pw(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000).hex()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/register", status_code=201)
def register(data: RegisterIn):
    if data.username in users:
        raise HTTPException(409, "Username already exists")
    salt = secrets.token_bytes(16)
    users[data.username] = {"salt": salt, "hash": hash_pw(data.password, salt)}
    return {"message": "User created"}


@app.post("/login")
def login(data: LoginIn):
    if failed.get(data.username, 0) >= MAX_FAILS:
        raise HTTPException(423, "Account locked")
    user = users.get(data.username)
    if not user or hash_pw(data.password, user["salt"]) != user["hash"]:
        failed[data.username] = failed.get(data.username, 0) + 1
        raise HTTPException(401, "Invalid credentials")
    failed[data.username] = 0
    token = secrets.token_hex(16)
    tokens[token] = data.username
    return {"access_token": token}


@app.get("/me")
def me(authorization: str = Header(default="")):
    token = authorization.removeprefix("Bearer ").strip()
    if token not in tokens:
        raise HTTPException(401, "Not authenticated")
    return {"username": tokens[token]}