from parse import parseJson

surv = parseJson('../survey.json')

question_id = 3
id = int(question_id) + 1 # cast to an int, comes in as a string
data = surv.question_metadata(id) # return first question

if data:
    print(data[0])
    print(data[1])
else:
    print('WRONG')
