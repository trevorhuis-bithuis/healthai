import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


class BaseConfig:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")
