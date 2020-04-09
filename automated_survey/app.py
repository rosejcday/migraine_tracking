import json

from flask import Flask, request
from flask import url_for, request, session
from twilio import twiml
from twilio.twiml.messaging_response import Message, MessagingResponse

from parse import parseJson

app = Flask(__name__)
surv = parseJson('../survey.json') # Survey JSON
# TODO: Remove to config
app.secret_key = 'thisisanoodle' # Session secret

# SMS instructions for question type
SMS_INSTRUCTIONS = {
        'text': 'Please type your answer.',
        'hours': 'Please type number of hours.',
        'numeric': 'Please type a number between 1 and 10.'
}

@app.route('/sms', methods=['Post'])
def sms_survey():
    """
    This is the first route to be reached when the code runs and a message comes in.
    At this point, the app will welcome the user and redirect them to the first question.
    After an answer has come in from the first question, the app will begin to redirect to the next question until finished.
    """
    response = MessagingResponse()

    if 'question_id' in session:
        response.redirect(url_for('answer', question_id=session['question_id']))
    else:
        welcome_user(response.message)
        redirect_to_first_question(response)
    return str(response)

def welcome_user(send_function):
    """
    Welcome the user to the survey .
    """
    welcome_text = 'Welcome, time to log a migraine!'
    send_function(welcome_text)

def redirect_to_first_question(response):
    """
    Redirect the user to the first question of the survey /question/1.
    """
    first_question, type = surv.question_metadata(1) # return first question

    first_question_url = url_for('question', question_id='1')
    response.redirect(url=first_question_url, method='GET')

@app.route('/question/<question_id>')
def question(question_id):
    """
    This route is meant for the questions and takes in the question_id as the input.
    The question_id tells the app what question it should respond back with using the `sms_twiml` function.
    This ID is taken in as a string and casted as an int in order to use the parse survey object to grab out the next question.
    The session keeps track of the question ID and Flask handles cookie management.

    :return: SMS response
    """
    id = int(question_id) # cast to an int, comes in as a string
    question, type = surv.question_metadata(id) # return first question
    print(question)
    print(type)
    session['question_id'] = id
    return sms_twiml(question, type)

def sms_twiml(question, type):
    """
    Takes in a question and returns the question and SMS instructions based on the type of response expected.
    Type of response is a section of the JSON that contains ID, question, and type.

    :return: SMS Response
    """
    response = MessagingResponse()
    response.message(question)
    response.message(SMS_INSTRUCTIONS[type])
    return str(response)


@app.route('/answer/<question_id>', methods=['POST'])
def answer(question_id):

    id = int(question_id) + 1 # cast to an int, comes in as a string
    data = surv.question_metadata(id) # return first question

    # Save answer to the question
    """db.save(Answer(content=extract_content(question),
                   question=question,
                   session_id=session_id()))"""
    if data:
        return redirect_twiml(id)
    else:
        return goodbye_twiml()


def extract_content(question):
    if is_sms_request():
        # return body of text
        return request.values['Body']
    else:
        # return digits from text
        return request.values['Digits']

def is_sms_request():
    return 'MessageSid' in request.values.keys()

def redirect_twiml(question_id):
    response = MessagingResponse()
    response.redirect(url=url_for('question', question_id=question_id), method='GET')
    return str(response)

def goodbye_twiml():
    response = MessagingResponse()
    response.message("Thank you for answering our survey. Goodbye!")

    if 'question_id' in session:
        del session['question_id']
    return str(response)

if __name__ == '__main__':
    app.run()
