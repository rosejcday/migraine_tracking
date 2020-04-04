from setuptools import setup

setup(
   name='automated_survey',
   version='1.0.0',
   description='A module to interface Twilio SMS surveys with Google Sheets API.',
   author='@rosejcday',
   packages=['automated_survey'],  #same as name
   install_requires=['gspread', 'oauth2client'], #external packages as dependencies
)
