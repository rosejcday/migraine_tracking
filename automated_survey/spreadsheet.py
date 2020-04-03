import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

# Use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('../client_secret.json', scope)
client = gspread.authorize(credentials)

# Find a workbook by name and open the first sheet
sheet = client.open("migraine_tracker").sheet1

# Insert new row of data
# Date	Severity 	Location 	Duration	Medication
migraine_data = ["4/3/2020","3","Eyes and Neck","2","None"]
index = 2
sheet.insert_row(migraine_data, index)

# Extract all of the values
list_of_hashes = sheet.get_all_records()

# Pretty print the output of the entire sheet
pp = pprint.PrettyPrinter()
pp.pprint(list_of_hashes)
