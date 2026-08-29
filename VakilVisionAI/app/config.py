from dotenv import load_dotenv
import os

load_dotenv()

# Get the environment variables
MONGO_URI = os.getenv("MONGO_URI")


ALLOWED_EXTENSIONS = ['.pdf', '.txt']  # Allowed file extensions for contract uploads

MAX_SIZE_MB = 10  # Maximum file size in megabytes for contract uploads

UPLOAD_DIR = "uploads"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")