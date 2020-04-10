import json
import os

from dotenv import load_dotenv
from parse import parseJson
from pathlib import Path  # python3 only

"""surv = parseJson('../survey.json')

question_id = 3
id = int(question_id) + 1 # cast to an int, comes in as a string
data = surv.question_metadata(id) # return first question

if data:
    print(data[0])
    print(data[1])
else:
    print('WRONG')"""


path=os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'twilio.env'))
load_dotenv(dotenv_path=path)
SECRET_KEY = os.getenv("APP_SECRET")
print(SECRET_KEY)
print(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '')))
