from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DJANGO_ENV = os.getenv("DJANGO_ENV", "dev")

env_file = ".env.dev" if DJANGO_ENV == "dev" else ".env.prod"
load_dotenv(dotenv_path=os.path.join(BASE_DIR, env_file))


ENV_VARIABLES = {
    "DB_NAME": os.getenv("DB_NAME"),
    "DB_USER": os.getenv("DB_USER"),
    "DB_PASSWORD": os.getenv("DB_PASSWORD"),
    "DB_HOST": os.getenv("DB_HOST", "localhost"),  # default if missing
    "DB_PORT": os.getenv("DB_PORT", "5432"),
    "SETTINGS": os.getenv("SETTINGS", "dev"),
    "TOKEN_SECRET_KEY": os.getenv("TOKEN_SECRET_KEY"),
    "ACCESS_TOKEN_EXPIRY": os.getenv("ACCESS_TOKEN_EXPIRY"),
    "ACCESS_TOKEN_SECRET": os.getenv("ACCESS_TOKEN_SECRET"),
    "REFRESH_TOKEN_SECRET": os.getenv("REFRESH_TOKEN_SECRET"),
    "REFRESH_TOKEN_EXPIRY": os.getenv("REFRESH_TOKEN_EXPIRY"),
    "DJANGO_ENV": os.getenv("DJANGO_ENV", "dev"),
}
print("print", env_file)
