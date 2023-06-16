from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID1 = ''
RANGE_NAME1 = ''

SPREADSHEET_ID2 = ''
RANGE_NAME2 = ''

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../secret/client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet1 = service.spreadsheets()
        result = sheet1.values().get(spreadsheetId=SPREADSHEET_ID1,
                                     range=RANGE_NAME1).execute()
        values1 = result.get('values', [])

        sheet2 = service.spreadsheets()
        result = sheet2.values().get(spreadsheetId=SPREADSHEET_ID2,
                                     range=RANGE_NAME2).execute()
        values2 = result.get('values', [])

        if not values1 or not values2:
            print('No data found.')
            return

        values1.sort()

        correct_number = pd.DataFrame(values1)

        df_labels = ['name', 'registration']

        correct_number = correct_number.rename(columns=dict(zip(correct_number.columns, df_labels)))

        correct_number = correct_number.dropna()

        to_rep = pd.DataFrame(values2)

        to_rep = to_rep.rename(columns=dict(zip(to_rep.columns, df_labels)))

        to_rep = to_rep.dropna()

        names = [name for name in to_rep['name'].values] \
                + [name for name in correct_number['name'].values if name not in to_rep['name']]

        names.sort()

        for name in names:
            if name not in correct_number['name'].values:
                correct_number = correct_number._append({'name': name, 'registration': 'M/N/F'}, ignore_index=True)
            if name in correct_number['name'].values and name not in to_rep['name'].values:
                correct_number = correct_number.drop(correct_number[correct_number['name'] == name].index)

        correct_number = correct_number.sort_values(by='name')

        correct_number = correct_number.reset_index(drop=True)

        to_rep = to_rep.sort_values(by='name')

        to_rep = to_rep.reset_index(drop=True)

        to_rep['registration'] = correct_number['registration'].where(correct_number['name'].str.strip() == to_rep['name'].str.strip())

        update_value = to_rep.values.tolist()

        sheet2.values().update(spreadsheetId=SPREADSHEET_ID2,
                            range=RANGE_NAME2, valueInputOption='RAW',
                            body={"values": update_value}).execute()

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
