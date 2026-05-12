import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]

for env_file in (PROJECT_ROOT / ".env", PROJECT_ROOT / ".env.py"):
    if env_file.exists():
        load_dotenv(env_file, override=True)
        break


class ConfigReader:
    BASE_URL = os.getenv("BASE_URL", "")
    USERNAME = os.getenv("PARABANK_USERNAME") or os.getenv("USERNAME", "")
    PASSWORD = os.getenv("PARABANK_PASSWORD") or os.getenv("PASSWORD", "")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT", "30000"))

    @classmethod
    def validate_login_config(cls) -> None:
        """Fail fast with a clear message when required env values are missing."""
        missing_values = []

        if not cls.BASE_URL:
            missing_values.append("BASE_URL")
        if not cls.USERNAME:
            missing_values.append("PARABANK_USERNAME or USERNAME")
        if not cls.PASSWORD:
            missing_values.append("PARABANK_PASSWORD or PASSWORD")

        if missing_values:
            missing_text = ", ".join(missing_values)
            raise ValueError(f"Missing required environment values: {missing_text}")
