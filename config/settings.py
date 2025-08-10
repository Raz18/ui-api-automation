from dataclasses import dataclass
import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Helper to parse booleans from env
_DEF_TRUE = {"1", "true", "yes", "on"}
_DEF_FALSE = {"0", "false", "no", "off"}

def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    val = raw.strip().lower()
    if val in _DEF_TRUE:
        return True
    if val in _DEF_FALSE:
        return False
    return default

@dataclass(frozen=True)
class UISettings:
    base_url: str = os.getenv("BASE_URL", "https://www.saucedemo.com")
    timeout: int = int(os.getenv("UI_TIMEOUT", "10000"))  # ms
    headless: bool = _env_bool("HEADLESS", True)
    slowmo: int = int(os.getenv("SLOWMO", "0"))  # ms delay between actions

@dataclass(frozen=True)
class APICallSettings:
    base_url: str = os.getenv("AIRPORT_GAP_BASE_URL", "https://airportgap.com/")
    timeout: int = int(os.getenv("API_TIMEOUT", "10000"))  # ms (Playwright uses ms for request context timeout)

@dataclass(frozen=True)
class Credentials:
    username: str = os.getenv("SAUCE_USERNAME", "standard_user")
    password: str = os.getenv("SAUCE_PASSWORD", "secret_sauce")

@dataclass(frozen=True)
class AirportData:
    expected_airports_csv: str = os.getenv(
        "AIRPORTS_EXPECTED",
        "Akureyri Airport,St. Anthony Airport,CFB Bagotville"
    )
    distance_from: str = os.getenv("AIRPORT_DISTANCE_FROM", "KIX")
    distance_to: str = os.getenv("AIRPORT_DISTANCE_TO", "NRT")

    @property
    def expected_airports(self):
        return [a.strip() for a in self.expected_airports_csv.split(',') if a.strip()]

ui_settings = UISettings()
api_settings = APICallSettings()
credentials = Credentials()
airports = AirportData()
