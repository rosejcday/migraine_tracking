from flask import Flask, request
from twilio import twiml
from flask import url_for, session
from twilio.twiml.messaging_response import Message, MessagingResponse

app = Flask(__name__)

@app.route('/sms', methods=['Post'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']
    response = MessagingResponse()
    response.message('Hello {}, you said {}'.format(number, message_body))
    return str(response)

if __name__ == '__main__':
    app.run()
