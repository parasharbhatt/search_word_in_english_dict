# English Dictionary Search

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-unittest-brightgreen)

A professional desktop English dictionary application built with Python and Tkinter. It provides fast local lookups, case-insensitive searches, numbered meanings, fuzzy spelling suggestions, and a clean, responsive interface.

## Features

- Search more than 49,000 dictionary entries
- Case-insensitive exact matches
- Multiple meanings for a word
- Fuzzy-match spelling suggestions
- Keyboard-friendly search with **Enter**
- Responsive Tkinter interface
- Fully local data with no API or internet dependency

## Requirements

- Windows 10 or later
- Python 3.10 or later

## Installation

```powershell
git clone https://github.com/parasharbhatt/search_word_in_english_dict.git
cd "English Dictionary Search"
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run

```powershell
python search_dict.py
```

## Tests

Run the complete test suite:

```powershell
python -m pytest tests/ -v
```

Generate XML, HTML, coverage, and GUI screenshot artifacts:

```powershell
python -m pytest tests/ --junit-xml=test-reports/results.xml --html=test-reports/report.html --self-contained-html --cov=. --cov-report=term-missing --cov-report=html:test-reports/coverage
```

The generated files are written to `test-reports/`:

- `results.xml` - machine-readable JUnit test report
- `report.html` - self-contained visual test report
- `coverage/index.html` - source coverage report
- `application-screenshot.png` - captured application interface (Windows desktop runs)

## Project Structure

```text
English Dictionary Search/
|-- search_dict.py
|-- data.json
|-- tests/
|   `-- test_SearchApp.py
|-- requirements.txt
|-- Jenkinsfile
|-- LICENSE
`-- README.md
```

## Build a Windows Executable

PyInstaller is used by the Jenkins pipeline:

```powershell
pyinstaller --noconsole --onefile --add-data "data.json;." --name "EnglishDictionarySearch" search_dict.py
```

The executable is written to `dist/`. The build command bundles `data.json` inside the executable, so no separate data file is required.

## Data Format

`data.json` is a JSON object whose keys are dictionary terms and whose values are arrays of meanings:

```json
{
  "river": [
    "A natural flowing watercourse."
  ]
}
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
