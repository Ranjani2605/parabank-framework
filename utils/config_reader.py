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
    USERNAME = os.getenv("PARABANK_USERNAME", "")
    PASSWORD = os.getenv("PARABANK_PASSWORD", "")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    TIMEOUT = int(os.getenv("TIMEOUT", "30000"))
