import os
import logging
from dotenv import load_dotenv
logger = logging.getLogger(__name__)
# Load environment variables from a .env file
load_dotenv()

# Database connection parameters
DATABASE_URL = os.getenv("DATABASE_URL")
