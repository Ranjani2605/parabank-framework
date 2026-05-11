# ParaBank Automation Framework 🏦

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pytest](https://img.shields.io/badge/Pytest-Test%20Framework-green?logo=pytest)
![Playwright](https://img.shields.io/badge/Playwright-Browser%20Automation-2EAD33?logo=playwright)
![Allure](https://img.shields.io/badge/Allure-Reporting-orange)
![Status](https://img.shields.io/badge/Status-Active-success)

## 📌 Description

ParaBank Automation Framework is a Python-based UI test automation project for the [ParaBank demo banking application](https://parabank.parasoft.com/parabank/index.htm).

The framework uses **Pytest** and **Playwright** to automate browser-based test scenarios such as login, account overview, account creation, fund transfers, loan requests, transaction search, customer care, and contact information updates.

It follows the **Page Object Model (POM)** design pattern to keep test code clean, reusable, and easy to maintain.

## ✨ Features

- Automated UI tests for key ParaBank workflows
- Page Object Model structure for maintainable test automation
- Playwright browser automation with Pytest integration
- Configurable test settings using environment variables
- HTML test reporting with `pytest-html`
- Allure report generation support
- Screenshot and tracing support for failed tests
- Reusable fixtures for browser context and page setup

## 🛠 Tech Stack

- **Python**
- **Pytest**
- **Playwright**
- **pytest-playwright**
- **Allure Pytest**
- **pytest-html**
- **python-dotenv**
- **Requests**

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/parabank-framework.git
cd parabank-framework
```

### 2. Create and activate a virtual environment

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

On macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers

```bash
playwright install
```

### 5. Create a `.env` file

Create a `.env` file in the project root:

```env
BASE_URL=https://parabank.parasoft.com/parabank/index.htm
PARABANK_USERNAME=your_username
PARABANK_PASSWORD=your_password
HEADLESS=false
TIMEOUT=30000
```

> Note: `.env` is ignored by Git to avoid committing local credentials or environment-specific values.

## ▶️ Usage

Run all tests:

```bash
pytest
```

Run tests in headless mode by setting this value in `.env`:

```env
HEADLESS=true
```

Then run:

```bash
pytest
```

Run a specific test file:

```bash
pytest tests/test_login.py
```

Run tests in parallel:

```bash
pytest -n auto
```

Generate an HTML report:

```bash
pytest --html=reports/report.html
```

Generate Allure results:

```bash
pytest --alluredir=reports/allure-results
```

Serve the Allure report:

```bash
allure serve reports/allure-results
```

## 📸 Screenshots Placeholder

Add screenshots or report previews here:

```text
screenshots/
├── test-report-preview.png
├── login-test.png
└── account-overview-test.png
```

Example Markdown:

```markdown
![Test Report](screenshots/test-report-preview.png)
```

## 📁 Folder Structure

```text
parabank-framework/
├── configs/              # Configuration package
├── data/                 # Test data package
├── pages/                # Page Object Model classes
├── tests/                # Pytest test cases
├── utils/                # Utility helpers and config readers
├── reports/              # Generated HTML and Allure reports
├── logs/                 # Runtime logs
├── conftest.py           # Shared Pytest fixtures
├── pytest.ini            # Pytest configuration
├── requirements.txt      # Python dependencies
├── .env                  # Local environment variables
├── .gitignore            # Git ignored files
└── README.md             # Project documentation
```

## 🔐 Environment Variables

| Variable | Description | Example |
| --- | --- | --- |
| `BASE_URL` | ParaBank application URL | `https://parabank.parasoft.com/parabank/index.htm` |
| `PARABANK_USERNAME` | Username used for login tests | `your_username` |
| `PARABANK_PASSWORD` | Password used for login tests | `your_password` |
| `HEADLESS` | Run browser in headless mode | `true` or `false` |
| `TIMEOUT` | Default Playwright timeout in milliseconds | `30000` |

## 📚 API Reference

This project is primarily a UI automation framework and does not expose custom API endpoints.

If API tests are added later, document them here using this format:

```http
GET /api/example
```

| Parameter | Type | Description |
| --- | --- | --- |
| `id` | `string` | Example resource identifier |

## ☁️ Deployment

This project is not deployed as a web application. It is intended to run locally or in a CI/CD pipeline.

Example CI command:

```bash
pip install -r requirements.txt
playwright install
pytest
```

Generated reports can be published as CI artifacts from:

```text
reports/report.html
reports/allure-results/
```

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature/your-feature-name
```

3. Make your changes
4. Run the test suite

```bash
pytest
```

5. Commit your changes

```bash
git commit -m "Add your meaningful commit message"
```

6. Push your branch and create a pull request

```bash
git push origin feature/your-feature-name
```

## 📄 License

This project is currently not licensed. Add a license file such as `MIT`, `Apache-2.0`, or another license before publishing the repository publicly.

## 👤 Author

**Your Name**

- GitHub: [@your-username](https://github.com/your-username)
- Project: ParaBank Automation Framework
