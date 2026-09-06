# AI/LLM Quality Engineering Framework

A comprehensive testing automation framework for validating AI/LLM outputs and prompt engineering quality.

## Project Structure

```
ai-quality-engineering/
├── src/                    # Core validation and utility modules
├── tests/                  # Test files (unit, integration, validation tests)
├── test_data/             # Test data, fixtures, sample prompts, and expected outputs
├── utils/                 # Helper utilities and common functions
├── reports/               # Test reports and coverage reports
├── .env                   # Environment variables (API keys, configuration)
├── .gitignore            # Git ignore rules
├── requirements.txt      # Python dependencies
├── pytest.ini           # Pytest configuration
└── README.md            # This file
```

## Pillar 1: Prompt & Output Validation

This framework starts with core capabilities for:
- **Prompt Validation**: Ensure prompts are well-formed and meet quality standards
- **Output Validation**: Verify LLM outputs against expected criteria (length, format, content)
- **Quality Metrics**: Basic quality scores and assertions
- **Test Data Management**: Organize and manage test cases and fixtures

## Setup Instructions

### 1. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Edit `.env` file and add your API keys:
```
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run with coverage report
```bash
pytest --cov=src --cov-report=html
```

### Run specific test file
```bash
pytest tests/test_prompt_validation.py
```

### Run with verbose output
```bash
pytest -v
```

### Run by marker
```bash
pytest -m unit
pytest -m validation
```

## Folder/File Descriptions

| Folder/File | Purpose |
|---|---|
| `src/` | Core modules for prompt and output validation |
| `tests/` | All test files organized by feature/pillar |
| `test_data/` | Test fixtures, sample prompts, and expected outputs |
| `utils/` | Helper functions, common utilities, test helpers |
| `reports/` | Generated test reports and coverage reports |
| `.env` | Sensitive environment variables (not versioned) |
| `.gitignore` | Specifies files to exclude from Git |
| `requirements.txt` | Python package dependencies |
| `pytest.ini` | Pytest configuration and test discovery settings |

## Next Steps

1. Add more validation modules to `src/`
2. Create test cases in `tests/`
3. Organize test data in `test_data/`
4. Extend with additional pillars (Hallucination Detection, Cost Analysis, etc.)

## Development

Always work within the virtual environment:
```bash
# Activate venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

Install new packages:
```bash
pip install <package_name>
pip freeze > requirements.txt  # Update requirements
```
