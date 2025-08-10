# ControlUp Automation Test Suite

A comprehensive automated testing solution demonstrating best practices in UI and API test automation using modern Python tooling. This project showcases professional-grade test architecture, emphasizing maintainability, scalability, and robust reporting capabilities.

## 📋 Project Overview

This test automation framework addresses the ControlUp technical assessment requirements by implementing both UI and API test scenarios with enterprise-level design patterns. The project demonstrates proficiency in:

- **Test Automation Architecture**: Implementing scalable Page Object Model (POM) patterns
- **API Testing Excellence**: Leveraging Playwright's APIRequestContext for robust API validation
- **Quality Engineering**: Comprehensive logging, reporting, and error handling mechanisms
- **DevOps Integration**: CI/CD ready configuration with environment-based test execution

### Purpose & Significance

Automated testing serves as the backbone of modern software development, ensuring:
- **Regression Prevention**: Continuous validation of application functionality
- **Quality Assurance**: Early detection of defects in the development lifecycle
- **Performance Optimization**: Efficient test execution through parallel processing
- **Documentation**: Living specifications through executable test scenarios

## 🛠 Technological Stack

### Core Testing Framework
- **Python 3.11+**: Modern language features with enhanced type hints and dataclasses
- **Playwright**: Next-generation browser automation with superior stability and performance
- **pytest**: Advanced testing framework with powerful fixtures and parameterization

### UI Testing Architecture
```python
# Playwright with sync API for consistent, reliable browser automation
from playwright.sync_api import Page, Locator, expect

# Role-based locator strategy for accessibility-first element selection
element = page.get_by_role("button", name="Add to cart")
```

### API Testing Infrastructure
```python
# Playwright APIRequestContext for HTTP testing
api_context = playwright.request.new_context(
    base_url="https://airportgap.com/api",
    extra_http_headers={"Accept": "application/json"}
)
```

### Supporting Technologies
- **python-dotenv**: Environment configuration management
- **pytest-html**: Rich HTML test reporting with screenshots
- **dataclasses**: Type-safe configuration objects with immutability
- **Custom Logging**: Structured logging with file and console output
- **Automatic Reporting**: Pytest hooks for seamless report generation
- **Screenshot Capture**: Failure screenshots with automatic directory creation

## 🏗 Design Principles

### 1. Page Object Model (POM) Architecture
```python
class BasePage:
    """Central base class providing wrapped Playwright actions with logging."""
    
    def click(self, target: Union[str, Locator], *, force: bool = False):
        loc = self._ensure_locator(target)
        self.logger.info(f"Click: {self._describe(loc)}")
        loc.click(force=force)
```

**Benefits:**
- **Maintainability**: Centralized element definitions and actions
- **Reusability**: Shared methods across all page objects
- **Debugging**: Comprehensive logging for troubleshooting

### 2. Configuration-Driven Testing
```python
@dataclass(frozen=True)
class UISettings:
    base_url: str = os.getenv("BASE_URL", "https://www.saucedemo.com")
    headless: bool = _env_bool("HEADLESS", True)
    slowmo: int = int(os.getenv("SLOWMO", "0"))
```

**Advantages:**
- **Environment Flexibility**: Easy switching between test environments
- **Immutable Configuration**: Thread-safe settings with `frozen=True`
- **Type Safety**: Compile-time validation with dataclasses

### 3. Semantic Locator Strategy
```python
# Accessibility-first approach
username_input = page.get_by_label("Username")
login_button = page.get_by_role("button", name="Sign in")

# Fallback to stable data attributes
fallback_locator = page.locator('[data-test="login-button"]')
```

### 4. Comprehensive Error Handling & Logging
```python
# Structured logging with context
logger = setup_logger("API_Tests")
logger.info(f"Making GET request to {endpoint}")

# Defensive JSON parsing with detailed error context
def safe_json_parse(response):
    """Defensive JSON parsing with detailed error context."""
    try:
        return response.json()
    except json.JSONDecodeError as e:
        body_preview = response.text()[:500]
        raise AssertionError(f"JSON decode error: {e}. Body: {body_preview}")
```

## 📁 Project Structure

```
ui_api_automation/
├── config/                 # Configuration management
│   ├── settings.py         # Environment-driven settings with dataclasses
│   └── __init__.py
├── pages/                  # Page Object Model implementation
│   ├── base_page.py        # Core page actions with logging
│   ├── login_page.py       # SauceDemo authentication
│   ├── inventory_page.py   # Product catalog interactions
│   └── __init__.py
├── tests/                  # Test suites organized by domain
│   ├── ui/                 # Browser-based test scenarios
│   │   └── test_inventory_ui.py
│   ├── api/                # HTTP API validation tests
│   │   └── test_airports_api.py
│   └── conftest.py         # Pytest fixtures and configuration
├── utils/                  # Shared utilities
│   ├── logger.py           # Structured logging setup
│   └── __init__.py
├── reports/                # Generated test reports (HTML/JSON)
├── logs/                   # Execution logs with timestamps
├── screenshots/            # Failure screenshots for debugging
├── .env                    # Environment variables (not in VCS)
├── pytest.ini             # Pytest configuration
├── requirements.txt        # Python dependencies
└── README.md
```

## 🧪 Testing Scenarios

### UI Test Scenarios (SauceDemo)
| Scenario | Description | Validation Points |
|----------|-------------|-------------------|
| **Inventory Validation** | Verify product catalog displays exactly 6 items | Item count, element visibility |
| **Cart Functionality** | Add single item and verify cart badge updates | State management, UI feedback |
| **Bulk Operations** | Add all items to cart and validate total count | Batch operations, consistency |

### API Test Scenarios (Airport Gap)
| Scenario | Description | Validation Points |
|----------|-------------|-------------------|
| **Data Integrity** | Verify API returns exactly 30 airport records | Response structure, count validation |
| **Content Validation** | Confirm presence of specific airports in dataset | Data completeness, search functionality |
| **Distance Calculation** | Validate distance between KIX and NRT airports > 400km | Mathematical accuracy, business logic |

## 🚀 Key Improvements & Advanced Features

### 1. Enhanced Browser Management
```python
# Multi-browser support with configurable options
@pytest.fixture(scope="session")
def browser(playwright_instance):
    return playwright_instance.chromium.launch(
        headless=ui_settings.headless,
        slow_mo=ui_settings.slowmo  # Visual debugging support
    )
```

### 2. Intelligent Error Recovery
```python
def click_with_retry(self, element, retries=3):
    """Resilient clicking with automatic retry logic."""
    for attempt in range(1, retries + 1):
        try:
            element.click()
            return
        except Exception as e:
            if attempt == retries:
                self.screenshot(f"error_click_{timestamp()}.png")
                raise
```

### 3. Comprehensive Reporting
- **HTML Reports**: Rich visual reports with test execution details
- **Screenshot Capture**: Automatic failure screenshots for debugging  
- **Performance Metrics**: Test execution timing and resource usage
- **Log Integration**: Structured logs linked to test results
- **Directory Management**: Automatic creation of reports/, logs/, and screenshots/ directories

### 4. CI/CD Integration Ready
```bash
# Environment-specific execution
export HEADLESS=true
export LOG_LEVEL=DEBUG
pytest -m api --html=reports/api_results.html

# Parallel execution for faster feedback
pytest -n auto --dist worksteal
```

## 🔧 Installation & Usage

### Prerequisites
- Python 3.11 or higher
- Node.js (for Playwright browser installation)

### Setup Instructions
```bash
# 1. Clone and navigate to project
git clone <repository-url>
cd ui_api_automation

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate.ps1  # Windows PowerShell

# 3. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 4. Configure environment (optional)
cp .env.example .env
# Edit .env with your preferred settings
```

### Execution Commands
```bash
# Run all tests with comprehensive reporting
pytest -v --html=reports/full_report.html

# Using the custom test runner script
python run_tests.py --type all                    # Run all tests
python run_tests.py --type ui --headed            # UI tests in visible browser
python run_tests.py --type api --no-report        # API tests without HTML report

# Domain-specific test execution
pytest -m ui -v                    # UI tests only
pytest -m api -v                   # API tests only

# Environment-specific runs
HEADLESS=false pytest -m ui        # Visual mode for debugging
SLOWMO=500 pytest -m ui           # Slow motion for demonstrations

# Parallel execution for performance
pytest -n auto                     # Auto-detect CPU cores
```

## 📊 Environment Configuration
| Variable | Default | Description | Example |
| `BASE_URL` | https://www.saucedemo.com | SauceDemo application URL | https://staging.saucedemo.com |
| `AIRPORT_GAP_BASE_URL` | https://airportgap.com/ | Airport Gap API base URL | https://api-v2.airportgap.com/ |
| `HEADLESS` | true | Browser visibility mode | false (for debugging) |
| `SLOWMO` | 0 | Action delay in milliseconds | 250 (for demonstrations) |
| `LOG_LEVEL` | INFO | Logging verbosity | DEBUG (detailed logs) |
| `SAUCE_USERNAME` | standard_user | SauceDemo login username | performance_glitch_user |
| `SAUCE_PASSWORD` | secret_sauce | SauceDemo login password | secret_sauce |

## 🔄 Continuous Integration

### GitHub Actions Example
```yaml
name: Automated Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: playwright install --with-deps chromium
      - run: pytest --html=reports/ci_report.html
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-reports
          path: reports/
```

## 📈 Performance Optimizations

- **Session-Scoped Fixtures**: Browser instances shared across test sessions
- **Parallel Execution**: Multi-threaded test execution with pytest-xdist
- **Smart Waits**: Explicit waits instead of sleep statements
- **Resource Management**: Automatic cleanup of browser contexts and pages

## 🤝 Contributing & Extension Guidelines

### Adding New Page Objects
```python
class NewPage(BasePage):
    """Template for new page implementations."""
    
    # Define locators as class constants
    SUBMIT_BUTTON = '[data-test="submit"]'
    
    def perform_action(self):
        """Implement business-specific actions."""
        self.click(self.SUBMIT_BUTTON)
        return self  # Enable method chaining
```

### API Test Extension
```python
@pytest.mark.api
def test_new_endpoint(api_request_context):
    """Template for API test implementation."""
    response = api_request_context.get("/new-endpoint")
    expect(response).to_be_ok()
    
    data = response.json()
    assert "expected_field" in data
```

## 📞 Support & Documentation

For technical questions or contribution guidelines:
- **Architecture Questions**: Review the `pages/base_page.py` implementation
- **Configuration Issues**: Check `.env` file and `config/settings.py`
- **Test Failures**: Examine logs in `logs/` directory and screenshots in `screenshots/`
- **Performance Tuning**: Adjust `pytest.ini` settings and environment variables

