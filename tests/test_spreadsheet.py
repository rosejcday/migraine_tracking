from automated_survey.spreadsheet import *
from os import path

import os.path
import pytest
import pprint

sheet1 = spreadsheet('client_secret.json', "migraine_tracker")
data = ["4/3/2020","3","Eyes and Neck","2","None"]

def test_path():
    """
    Determine if the path specified is correct.
    """
    assert path.exists('client_secret.json')

def test_initalized_sheet():
    """
    Determine if a sheet initalized.
    """
    assert sheet1
    assert "Sheet has been initialized."

def test_data_manipulation():
    """
    Determine if data can be manipulated within the sheet.
    """
    sheet1.insert_data(data)
    assert "Data has been inserted into the sheet."
    returned = sheet1.return_data()
    assert "Data has been returned from the sheet."
    sheet1.delete_data()
    assert "Data has been deleted from the sheet."

def test_wrong_path():
    """
    Determine that the try/catch works when wrong path or sheet has been declared.
    """
    sheet1 = spreadsheet('../client_secret.json', "migraine_tracker")
    assert "Wrong path has been declared."
    sheet1 = spreadsheet('client_secret.json', "migrainetracker")
    assert "Wrong sheet name has been declared."

def test_data_manipulation_issues():
    """
    Determine that the try/catch works when there are issues deleting or inserting data.
    """
    sheet1.delete_data()
    sheet1.delete_data()
    assert "Data has been deleted from the sheet."
    returned = sheet1.insert_data("data")
    assert "Data has been returned from the sheet."
