import gspread
from oauth2client.service_account import ServiceAccountCredentials

class spreadsheet(object):

    def __init__(self, json: str, sheet_name: str):
        """
        Use credentials proviced to create a client to interact with the Google Drive API.

        :param json: JSON configuration file from Google API.
        :param sheet_name: Name of the sheet to manipulate in Google Drive.
        """
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(json, scope)
            self.client = gspread.authorize(credentials) # client for Google Drive API
            self.sheet = self._open_first_sheet(sheet_name) # Sheet that is opened
        except:
            print("There appears to be an issue with the provided sheet name or JSON credentials, please review and try again.")

    def _open_first_sheet(self, sheet_name: str):
        """
        Find the specified workbook by name and open the first sheet.

        :param sheet_name: Name of the sheet to manipulate in Google Drive.
        :return: client for the Google Drive API.
        """
        try:
            return self.client.open(sheet_name).sheet1
        except:
            print("There appears to be an issue finding the sheet {}.".format(sheet_name))

    def insert_data(self, data: list, index: int = 2):
        """
        Insert data provided into the sheet.

        :param data: List of data elements to insert into the sheet.
        :param index: Index to insert data into. Defaults to index 2, assuming the first index has headers.
        """
        try:
            self.sheet.insert_row(data, index)
        except:
            print('Cannot append data to sheet.')

    def delete_data(self, index: int = 2):
        """
        Delete a row of data in the sheet.

        :param index: Index to delete row of data. Defaults to index 2, assuming the first index has headers and the most current data was placed at index 2.
        """
        if self.return_data():
            self.sheet.delete_row(index)

    def return_data(self):
        """
        Return all data extracted from the sheet.

        :return: A JSON of all the data stored in the sheet.
        """
        return self.sheet.get_all_records()
