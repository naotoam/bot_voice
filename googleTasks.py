from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']


def getLists():
    # service.tasklists().list(maxResults=10).execute()
    # items = results.get('items', [])
    lists = connectApiTask().tasklists().list(maxResults=10).execute()
    return lists.get('items', [])

def connectApiTask():
    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('tokentasks.json'):
        creds = Credentials.from_authorized_user_file('tokentasks.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
               '.vscode/client_secret_308627102332-jbtm6dig1g1ptuemsvn80sburbcr3nbq.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('tokentasks.json', 'w') as token:
            token.write(creds.to_json())

    service = build('tasks', 'v1', credentials=creds)

    # Call the Tasks API
    return service
    # results = service.tasklists().list(maxResults=10).execute()
    # items = results.get('items', [])
    # tareas = service.tasks().list(tasklist=items[0]["id"]).execute().get('items', [])
    # print("tareas?", tareas)
    # if not tareas:
    #     print('No task lists found.')
    # else:
    #     print('Task lists:')
    #     for item in tareas:
    #         #print(u'{0} ({1})'.format(item['title'], item['id']))
    #         print(item["title"], item["updated"])

if __name__ == '__main__':
    getLists()