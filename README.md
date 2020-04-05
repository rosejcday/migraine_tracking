# Automated Survey with for Tracking Migraines

## Quickstart

### Technologies

Python 3

### Local development

1. Clone this repository and `cd` into it.

1. Go to Google API Manager https://console.developers.google.com/. Then add Google Drive API to our project which will allow us to access spreadsheet inside of Google Sheets for our account. Once that’s added, we need to create some credentials to access the API so click on ***Add Credentials*** on the next screen you see after enabling the API. This JSON file should be added to the root directory of the repository.

1. Install the requirements.

    ```bash
    pip3 install -r requirements.txt
    ```

1. Run the code.

  ```bash
  cd automated_survey
  python3 executor.py  
  ```

1. Run tests.

    ```bash
    python3 -m pytest tests/
    ```

1. Run coverage report.

  ```bash
  pytest --cov=automated_survey tests/ --cov-report html
  ```
