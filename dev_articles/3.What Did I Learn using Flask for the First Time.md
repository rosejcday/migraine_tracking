![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/i2qep1xvgg0gb7bpcbf4.png)

**16 April 2020**

Happy Thursday! I hope things are going well. I have enjoyed working through some (ha, many) issues while learning Flask to integrate Python with Twilio's API. This week I will focus on the issues and learnings I had with using both Flask and Twilio for the first time.

## Quick Recap

At the moment, I spend time logging migraines for the doctors office but don't remember the format she wanted, or the details she found important. This application is being created as a way to request a survey for a migraine through SMS, quickly fill out the details, and log the data for later use at the doctors appointment.

### Link to Code

To clone the code, please visit the GitHub project [here](https://github.com/rosejcday/migraine_tracking). This project is a current work in progress and is not fully functional at this time, the app will walk through a survey but data is not currently saved anywhere.

## Issues and Learnings

### Port Issues

The first issue I ran into was connecting to a port when starting my application using `python3 -m app run`. I have run into this issue in the past when I use to work on servers and would get similar messages to the one below.

```bash
socket.error: [Errno 48] Address already in use
```

This just means a process is bound to the port I am trying to use. This is caused by the same Python app being called before and that process still being bound to the port. To fix this, I looked at what Python processes were still running using `ps -fA | grep python`.

Using this, you can spot the running Python process that is still active. You may want to test if `http://localhost:<port>/` still shows a directory listing for local files. The second number is the process number that you will need to stop. This can be done using the command `kill` as in the example below:  

```bash
ps -fA | grep python

>>  501 39548 16817   0  9:50PM ttys001    0:00.20 Python -m app run

kill 39548

>> [1]+  Terminated: 15          python3 -m app run
```

***

> What did I learn here? **This is caused by the same Python app being called before and that process still being bound to the port.** This has only happened twice so far, and it is a simple and quick fix to just kill the process.

***

### Type and Casting

The next issue was one I didn't realize was happening until I ran into it. When running the application, I would answer the first question sent by the survey and received the response below:

```bash
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
127.0.0.1 - - [08/Apr/2020 18:09:20] "POST /sms HTTP/1.1" 200 -
[2020-04-08 18:09:20,296] ERROR in app: Exception on /question/1 [GET]

TypeError: cannot unpack non-iterable NoneType object
127.0.0.1 - - [08/Apr/2020 18:09:20] "GET /question/1?
```

After an initial search into this issue, it was clear that results were all over the place. With that, I looked into the first question and coded up what I expected to be happening. I set the `question_id` to 1, read in the JSON for the survey, and passed the question ID into the survey to grab the question information for it. After returning the first question and its type, I printed the information.

```python
from parse import parseJson

question_id = 1
surv = parseJson('../survey.json')
question, type = surv.question_metadata(question_id)
print(question)
print(type)
```

When running this code, it produced the expected results, therefore something was wrong with the way the `question_id` was being passed. To recreated the problem outside of the Flask application, I changed the `question_id` to a string instead of int. Rerunning that code, reproduced the expected error:

```bash
TypeError: cannot unpack non-iterable NoneType object
```

***

> What did I learn here? Therefore, the issue had been resolved. It was a type issue in which I was expecting an integer and receiving a string instead. **Don't assume the type of the value being passed in, make it explicit.**

***

### Flask Session Secrets

As I had mentioned, I have not used Flask before, so I expected to end up with issues learning how to use it. The main issue I had when learning Flask was how to use session secrets. After resolving the above issues, the next that came up was the about not having a session secret setup.

```bash
    "The session is unavailable because no secret "
RuntimeError: The session is unavailable because no secret key was set.  Set the secret_key on the application to something unique and secret.
```

Sessions allow you to store user data from one request to the next. This was needed in the survey in order to store and track the question that the user was on and iterate to the next question.

***

> What did I learn here? When researching sessions, **I learned that the secret key is used in a session to implement on top of the cookies and is used so that the data cannot be modified without the key used for signing.** Here is more information on [Sessions](https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions).

***

### Getting to the Next Question

The last issue I had came about when I was interacting with the code I developed previously to grab the JSON survey and read it. When implementing this code and trying to get to the next question in the survey, I ran into two main problems I had when working with the survey questions:

1. How to find out if there was another question in the JSON or not based on the currently stored `question_id`?  
2. What does the app do if there is another question? What does the app do if there is not another question?

With that, let's take a look at question 1, how do you use `question_id` to determine if another question exists. To start, I looked back at the function I created in `parse.py` to see how I was gathering the data and was using a filter object which grabbed out the question whose ID matched and would return the body and type of the data.

```python
 try:
            survey_dict = self._json_to_dict()['questions']
            data = list(filter(lambda item: item['id'] == question_id, survey_dict))

            if data:
                return data[0]['body'], data[0]['type']
        except:
            print("The index povided for the question does not appear to exist.")
```

After some further reading into this section of the code, I changed the line that filters to a way that will return a list instead of filter object. The line `filter(function, iterable)` is equivalent to `[item for item in iterable if function(item)]` which means I can change the code to substitute:

```python
data = [item for item in survey_dict if (item['id'] == question_id)]
```

This is a more Pythonic way to find the next question in the JSON that we read in.

With that, we can get onto question 2, what does the app do now that it has the data for the next question? The data returned for the next question is either `None` or the next question's information. Using the `question_id`, the `answer()` function reads in the question ID given, (example: question 1 returns 1) and then iterates to the next questions ID by 1. Therefore, when question 1 is provided, the next ID would be 2. We use that ID, 2, and feed it into the `surv.question_metadata()` function which looks to see if the data returned is None or another question.

Before proceeding with that data collected, the `answer()` function extracts out the content from the previous question and stores it, which will be discussed more next week. After storing the data, the function looks to see if the data for the next question is None, which will end the survey, OR the if the data contains the next question, it will then pass the ID of the question and pass the ID to `redirect_twiml()` which will handle the response to the user.    

```python
@app.route("/answer/<question_id>", methods=["POST"])
def answer(question_id):

    id = int(question_id) + 1 # Cast to an int, comes in as a string
    data = surv.question_metadata(id) # Return first question
    data_collected.append(str(extract_content())) # Append the data collected

    if data:
        return redirect_twiml(id)
    else:
        return goodbye_twiml()
```

***

> What did I learn here? After working through these two problems, I gained a better understanding in how Flask operates to redirect from one function to the next and how I needed to setup the survey to redirect correctly as the user answered each question. During this time, I began to understand more about `Sessions` as well, which I talked about earlier. **The smallest tidbit of info I took away from this issue was that the line `filter(function, iterable)` is equivalent to `[item for item in iterable if function(item)]` which is a more Pythonic way to work with the data.**

***

### Development Stack

So far, I have worked on the code needed to interact with Google Sheets API and Twilio API in a Flask application...

![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/y77x1q2oufbxi3yw5buj.png)

Stay tuned for next weeks post where I discuss how I integrate the two API's together in the Python Flask app that generates a survey for migraines. I look forward to sharing with you the issues and learnings I have encountered while learning to use Flask with these API's!

## Additional Resources  

### Reference Links
[Twilio's Rest API](https://www.twilio.com/docs/usage/api)
[Automated Survey - Python Flask App](https://www.twilio.com/docs/voice/tutorials/automated-survey-python-flask)
[GitHub Sample Automated Survey](https://github.com/TwilioDevEd/automated-survey-flask)
[ngrok](https://ngrok.com/docs)
[How to Receive an SMS in Python with Twilio](https://www.youtube.com/watch?v=cZeCz_QOoXw&list=PLqrz4nXepkz63z1y4-oHfZHWy11gSoAn0&index=17)
[SMS Conversation Tracking](https://www.twilio.com/blog/2014/07/the-definitive-guide-to-sms-conversation-tracking.html)
