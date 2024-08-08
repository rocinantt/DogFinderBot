import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Database connection parameters
DATABASE_URL = os.getenv("DATABASE_URL")
