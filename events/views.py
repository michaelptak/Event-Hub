from django.shortcuts import render
from django.conf import settings
import requests
from datetime import datetime

# Create your views here.
def index(request):
    # Initialize variables that will be passed to the template
    processed_events = []
    search_performed = False

    # Check if the user submitted a search by looking for query parameters
    classification_name = request.GET.get('classificationName')
    city = request.GET.get('city')

    # If both search parameters are provided, perform search
    if classification_name and city:
        search_performed = True

        # Fetch events from Ticketmaster API
        raw_events_data = get_ticketmaster_events(classification_name, city)

        # Process the events if data was returned successfully
        if raw_events_data and raw_events_data.get('_embedded') and raw_events_data['_embedded'].get('events'):
            raw_events_list = raw_events_data['_embedded']['events']

            # Extract and format data from each event
            for event in raw_events_list:
                try:
                    # Parse datetime from ISO format
                    event_datetime_str = event['dates']['start']['dateTime']
                    event_datetime = datetime.fromisoformat(event_datetime_str.replace('Z', '+00:00'))

                    # Create simplified event dictionary matching model and cartd fields
                    processed_event = {
                        'event_id': event['id'],
                        'name': event['name'],
                        'image': event['images'][0]['url'],
                        'datetime': event_datetime, # Unformatted date time object for DB
                        'formatted_date': event_datetime.strftime('%a %b %d %Y'),
                        'formatted_time': event_datetime.strftime('%I:%M:%S %p'),
                        'url': event['url'],
                        'venue_name': event['_embedded']['venues'][0]['name'],
                        'venue_address': event['_embedded']['venues'][0]['address']['line1'],
                        'venue_city': event['_embedded']['venues'][0]['city']['name'],
                        'venue_state': event['_embedded']['venues'][0]['state']['name'],
                    }

                    processed_events.append(processed_event)

                except (KeyError, IndexError, ValueError):
                    # Skip events with missing or invalid data
                    continue

    # Create context dictionary with all data to pass to the template
    context = {
        'events': processed_events,
        'event_count': len(processed_events),
        'search_performed': search_performed,
    }

    # Render the template with context data
    return render(request, 'index.html', context)

def get_ticketmaster_events(classification_name, city):
    try:
        # Get the API key from settings
        api_key = settings.TICKETMASTER_API_KEY

        # Construct the Ticketmaster API URL
        ticketmaster_url = 'https://app.ticketmaster.com/discovery/v2/events.json'

        # Set up the query parameters
        params = {
            'apikey': api_key,
            'classificationName': classification_name,
            'city': city,
            'sort': 'date,asc'
        }

        # Send a GET request to the Ticketmaster API
        response = requests.get(ticketmaster_url, params=params)

        # Raise an exception for 4xx and 5xx status codes
        response.raise_for_status()

        # Parse the JSON data from the response
        data = response.json()

        # Return the parsed data
        return data
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network issues, timeouts)
        print(f"Ticketmaster API request failed: {e}")

        # Return None to indicate failure
        return None
