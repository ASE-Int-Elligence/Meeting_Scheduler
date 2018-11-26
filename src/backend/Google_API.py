from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import re
from config import *
import requests

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'

def get_credentials():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return creds

def get_calendar_events(creds, span_days):
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    end = (datetime.datetime.utcnow() + datetime.timedelta(days=span_days)).isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=end, singleEvents=True).execute()
    events = events_result.get('items', [])
    return events

def create_event(creds, title, start, end, attendees_emails="", location="", description=""):
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    event = {
        'summary': title,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start.isoformat(),
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end.isoformat(),
            'timeZone': 'America/New_York',
        },
        'attendees': [{'email': e} for e in attendees_emails],
    }
    event = service.events().insert(calendarId='primary', body=event).execute()

def get_event_location_map(event, width=600, height=450):
    print(event)
    event_location =re.sub("&", "", event["location"]) 
    ifram_str = f'<iframe width="{width}" height="{height}" frameborder="0" style="border:0" src="https://www.google.com/maps/embed/v1/place?key={Google_Map_Embed_API_KEY}&q={event_location}" allowfullscreen></iframe>'
    return ifram_str

def get_current_location_map(width=600, height=450):
    freegeoip = f"http://api.ipstack.com/check?access_key={ipstack_API_KEY}"
    geo_r = requests.get(freegeoip)
    geo_json = geo_r.json()
    # print(geo_json)
    # user_postition = [geo_json["latitude"], geo_json["longitude"]]
    lat = geo_json["latitude"]
    long = geo_json["longitude"]
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{long}&key={Google_Map_Embed_API_KEY}"
    print(geocode_url)
    geocode_r = requests.get(geocode_url)
    geocode_json = geocode_r.json()
    address = geocode_json["results"][0]["formatted_address"]
    ifram_str = f'<iframe width="{width}" height="{height}" frameborder="0" style="border:0" src="https://www.google.com/maps/embed/v1/place?key={Google_Map_Embed_API_KEY}&q={address}" allowfullscreen></iframe>'
    return ifram_str
    
    # url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={Google_Map_Embed_API_KEY}'
    # PARAMS = {'address':location} 
    # print(url)

if __name__ == '__main__':
    # main()
    creds = get_credentials()
    events = get_calendar_events(creds, 7)
    # print(get_event_location_map(events[4]))
    print(get_current_location_map())
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])

    # create_event(creds, "create a new event", 
    # datetime.datetime.now()+datetime.timedelta(days=1), 
    # datetime.datetime.now()+datetime.timedelta(days=1, hours=1),
    # attendees_emails=["user1@gmail.com", "user2@gmail.com"])

    # events = get_calendar_events(creds, 7)
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])
   