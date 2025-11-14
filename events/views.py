from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import requests

# Create your views here.
def index(request):
    return render(request, 'index.html')

def search_events(request):
    # Check if the request method is GET
    if request.method == 'GET':
        # Get the search parameters from query string
        classification_name = request.GET.get('classificationName')
        city = request.GET.get('city')

        # Validate that both parameters are provided
        if not classification_name or not city:
            return JsonResponse({'error': 'Both classification name and city are required fields.'},status=400)

        # Call the helper function to fetch events from Ticketmaster API
        events_data = get_ticketmaster_events(classification_name, city)

        # If the API request failed or returned None
        if events_data is None:
            return JsonResponse({'error': 'The server encountered an issue while fetching data. Please try again later.'}, status=500)

        # Return the events data as JSON
        return JsonResponse(events_data, safe=False)


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
