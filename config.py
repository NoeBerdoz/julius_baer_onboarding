import os

from dotenv import load_dotenv

load_dotenv()
API_URI = str(os.getenv("API_URI") or "")
API_KEY = str(os.getenv("API_KEY") or "")
API_TEAM = str(os.getenv("API_TEAM") or "")