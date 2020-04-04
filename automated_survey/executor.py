from spreadsheet import spreadsheet
import pprint

# Date	Severity 	Location 	Duration	Medication
data = ["4/3/2020","3","Eyes and Neck","2","None"]
sheet1 = spreadsheet('../client_secret.json', "migraine_tracker")
#sheet1.delete_data()
#sheet1.insert_data(data)
returned = sheet1.return_data()
# Pretty print the output of the entire sheet
pp = pprint.PrettyPrinter()
pp.pprint(returned)
