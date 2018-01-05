import os
import pickle
import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

import gspread

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_credentials():
    try:
        credentials = pickle.loads(open("sheets_token", "r").read())
        if credentials.expiry > (datetime.datetime.now() + datetime.timedelta(seconds=60)):
            return credentials
        else:
            print 'The credentials have expired'
    except Exception as e:
        pass
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    with open("sheets_token", 'w') as fp:
        fp.write(pickle.dumps(credentials))
    return credentials

def get_authenticated_service():
    credentials = get_credentials()
    # gspread looks for token in the wrong location
    credentials.access_token = credentials.token
    return gspread.authorize(credentials)

def run(gc):
    resource = gc.open_by_url('https://docs.google.com/spreadsheets/d/1Be........................MAc/edit') # copy and paste the google sheet URL here
    sheet = resource.get_worksheet(0)
    print 'Getting data'
    data = sheet.get_all_values()
    print 'Getting data done'
    header = data[0]
    for i, row in enumerate(data[1:]):
        i = i + 2
        val_1, val_2 = row
        if val_1.startswith('red'):
            print 'found row: %s' % repr(row)

            # sanity check to ensure the row matches what we are expecting
            assert sheet.cell(i, 1).value == val1

            # sanity check to ensure the cell is empty (so we dont overwrite something else)
            assert sheet.cell(i, 2).value == ''
            sheet.update_cell(i, 2, 'my-new-value')


if __name__ == '__main__':
  # When running locally, disable OAuthlib's HTTPs verification. When
  # running in production *do not* leave this option enabled.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  service = get_authenticated_service()
  run(service)
