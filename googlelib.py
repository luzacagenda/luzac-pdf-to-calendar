#!/usr/bin/env python

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

def get_credentials(CLIENT_SECRET_FILE, SCOPES, APPLICATION_NAME):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-luzac.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        flags = tools.argparser.parse_args(args=[])
        credentials = tools.run_flow(flow, store, flags)
        print('[*] Storing credentials to ' + credential_path)
    return credentials

def addEvent(id, eventData, client_secret, scopes, calendar):

    # Authenticate.
    credentials = get_credentials(client_secret, scopes, "Luzac Agenda")

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)




    event = service.events().insert(calendarId=calendar, body=eventData).execute()
    print('[*] Event created: ', event.get('htmlLink'))

def test(CLIENT_SECRET_FILE, SCOPES, APPLICATION_NAME):
    credentials = get_credentials(CLIENT_SECRET_FILE, SCOPES, APPLICATION_NAME)

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
