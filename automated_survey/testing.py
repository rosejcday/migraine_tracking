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

data_collected = [12015142415, 18604804670, '2020-04-10', 3, 'Neck and lower left side back of head', 2, 'None', 'Tired and stomach hurts']
results = [str(i) for i in data_collected] # Make sure all elements in list are strings
print(results)
