# Weather Dashboard - Testing Guide

This document explains the testing strategy and how to run tests for the Weather Dashboard project.

## Testing Overview

The project uses comprehensive testing with the following types:

### 1. Unit Tests
- **test_weather_api.py**: Tests the WeatherAPI class for fetching weather data
- **test_data_handler.py**: Tests the DataHandler class for CSV operations and statistics
- **test_ml_prediction.py**: Tests the WeatherPredictor class for ML model training and predictions

### 2. Integration Tests
- **test_integration.py**: Tests the complete workflow from API fetch to ML predictions

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures and configuration
├── test_weather_api.py      # WeatherAPI unit tests
├── test_data_handler.py     # DataHandler unit tests
├── test_ml_prediction.py    # WeatherPredictor unit tests
└── test_integration.py      # Integration tests
```

## Dependencies

Testing requires additional packages:
- pytest==7.4.0
- requests-mock==1.11.0

Install with:
```bash
pip install -r requirements.txt
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_weather_api.py
```

### Run Tests with Coverage
```bash
pytest --cov=src --cov-report=html
```

### Run Integration Tests Only
```bash
pytest -m integration
```

### Run Tests in Verbose Mode
```bash
pytest -v
```

## Test Coverage

The tests cover:

### WeatherAPI Tests
- ✅ API key validation
- ✅ Current weather fetching (success/error cases)
- ✅ Forecast fetching
- ✅ Error handling (network issues, invalid cities)

### DataHandler Tests
- ✅ CSV file loading
- ✅ City statistics calculation
- ✅ Weather record saving
- ✅ Error handling for missing files

### WeatherPredictor Tests
- ✅ Model initialization
- ✅ Training from historical data
- ✅ Temperature prediction
- ✅ Rain probability prediction
- ✅ Weather summary generation
- ✅ Edge cases (insufficient data, missing columns)

### Integration Tests
- ✅ Complete workflow: API → Save → Train → Predict
- ✅ Data analysis pipeline
- ✅ Cross-module interactions

## Mocking Strategy

- **API Calls**: Mocked using `unittest.mock` to avoid real API calls
- **File Operations**: Use temporary files for CSV operations
- **Environment Variables**: Mocked for API key testing

## Test Data

Tests use realistic sample data including:
- Multiple cities (London, Paris, Berlin)
- Various weather conditions (Clear, Clouds, Rain)
- Different temperature/humidity ranges
- Historical data for ML training

## CI/CD Integration

Tests are designed to run in automated environments:
- No external dependencies required
- Fast execution (< 30 seconds)
- Deterministic results
- Comprehensive error reporting

## Adding New Tests

When adding new features:

1. Create unit tests for new functions/methods
2. Add integration tests for new workflows
3. Update fixtures in `conftest.py` if needed
4. Ensure test coverage > 80%

## Running Tests on Windows

Use the provided `run_tests.bat` script:

```batch
run_tests.bat
```

Or manually:
```bash
cd weather_dashboard_project
python -m pytest tests/
```