import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils import validate_header_rules, update_data_into_sql, header_rule

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """
    Scipt fetched the authentication token for the first time from the Gmail
    Stores it to token json
    Trying to fetch gmail for the specified rule
    Sample data:
    [['HappyFox - Assignment', '"Sharon Samuel | HappyFox" <sharon@happyfox.hire.trakstar.com>', 'Fri, 16 Jun 2023 13:12:11 +0000 (UTC)']]
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/thiyageshdhandapani/Documents/Thiyagesh_code/fetch_mails/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Fetch Inbox data from Gmail API
        service = build('gmail', 'v1', credentials=creds)
        nextpagetoken = None
        filtered_gmail_data = []
        filtered_gmail_data = [['HappyFox - Assignment', 'Sharon Samuel | HappyFox <sharon@happyfox.hire.trakstar.com>', 'Fri, 16 Jun 2023 13:12:11 +0000 (UTC)']]
        while not filtered_gmail_data:
            result = service.users().messages().list(userId='me', q='in:inbox', pageToken=nextpagetoken).execute()
            messages = result.get('messages')
            for msg in messages:
                txt = service.users().messages().get(userId='me', id=msg['id']).execute()
                try:
                    payload = txt['payload']
                    headers = payload['headers']
                    status = validate_header_rules(headers)
                    if not status:
                        continue
                    filtered_gmail_data.append([i['value'].replace('"', '') for i in headers if i['name'] in header_rule])

                except Exception as e:
                    pass
            nextpagetoken = result.get('nextPageToken', None)
        if filtered_gmail_data:
            update_data_into_sql(filtered_gmail_data)
    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
