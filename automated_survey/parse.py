import json

class parseJson(object):

    def __init__(self, survey_json: str):
        """
        Read file of JSON and create a Python dictionary and associated metadata.

        :param survey_json: Filepath of the JSON
        """
        self.survey_json = survey_json

    def _json_to_dict(self):
        """
        Read file of JSON and create a Python dictionary

        :return: Python dictionary of the contents
        """

        # Open the JSON file
        with open(self.survey_json, 'r') as file:
            json_text = file.read()

        # Decode the JSON string into a Python dictionary.
        return json.loads(json_text)

    def question_metadata(self, question_id: int):
        """
        Take the contents of the JSON and find the question based on a given ID.

        :param question_id: ID of the question being looked for.
        :return: Metadata related to the question and type of response.
        """
        try:
            survey_dict = self._json_to_dict()['questions']
            data = list(filter(lambda item: item['id'] == question_id, survey_dict))

            if data:
                return data[0]['body'], data[0]['type']
        except:
            print("The index povided for the question does not appear to exist.")
