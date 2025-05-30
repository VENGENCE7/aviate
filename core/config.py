import os
from typing import Dict
from dotenv import load_dotenv
from core.constants.env_variables import ENV_VARIABLES

class AppConfig:
    SECRET_KEY: str
    DEBUG: bool
    DATABASE: Dict[str, str]

    def __init__(self) -> None:
        load_dotenv()
        self.validate_env_vars()

        self.SECRET_KEY = os.getenv('SECRET_KEY', '')
        self.DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')

        self.DATABASE = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', ''),
            'USER': os.getenv('DB_USER', ''),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', ''),
            'PORT': os.getenv('DB_PORT', ''),
        }

    def validate_env_vars(self) -> None:
        missing_vars = [var for var in ENV_VARIABLES if os.getenv(var) is None]
        if missing_vars:
            missing = ", ".join(missing_vars)
            raise EnvironmentError(
                f"Missing required environment variables: {missing}"
            )
        print("✅ All required environment variables are set.")


config = AppConfig()
