import os 
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'RnaOAShB7kMXOOdOYPKCJNxO')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///mydatabase.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
    GOOGLE_DISCOVERY_URL = os.environ.get("GOOGLE_DISCOVERY_URL")
    REDIRECT_URI = os.environ.get("REDIRECT_URI")
    TOKEN_URI = os.environ.get("TOKEN_URI")
    AUTH_URI = os.environ.get("AUTH_URI")
    API_BASE_URL = os.environ.get("API_BASE_URL")