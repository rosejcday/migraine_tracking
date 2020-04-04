import pytest
from automated_survey.spreadsheet import *
import pprint

sheet1 = spreadsheet('../client_secret.json', "migraine_tracker")
data = ["4/3/2020","3","Eyes and Neck","2","None"]

def test_initalized_sheet():
    assert sheet1

def test_insert_data():
    assert sheet1.insert_data(data)

"""def test_delete_data():
    assert sheet1.delete_data()
    returned = sheet1.return_data()
    assert [] == returned

def test_return_data():
    sheet1 = spreadsheet('../client_secret.json', "migraine_tracker")
    data = ["4/3/2020","3","Eyes and Neck","2","None"]
    returned = sheet1.return_data()
    assert returned == None
"""
