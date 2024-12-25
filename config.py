from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    # Required Telegram API credentials
    API_ID = os.getenv('API_ID')
    API_HASH = os.getenv('API_HASH')
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    
    # GitHub configuration_
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required = {
            'API_ID': cls.API_ID,
            'API_HASH': cls.API_HASH,
            'BOT_TOKEN': cls.BOT_TOKEN
        }
        
        missing = [key for key, value in required.items() if not value]
        
        if missing:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing)}\n"
                "Please check your .env file and ensure all required values are set."
            )
