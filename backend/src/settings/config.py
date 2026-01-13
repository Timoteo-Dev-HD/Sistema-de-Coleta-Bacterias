from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
    os.makedirs("uploads", exist_ok=True)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024