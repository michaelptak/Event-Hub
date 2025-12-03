from django.shortcuts import redirect, render
from django.conf import settings
import requests
import json
from datetime import datetime
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse, HttpResponseBadRequest
from .models import FavoriteEvent

# Create your views here.
def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def favorites_view(request):
    # Get all favorites for the current user
    favorite_events = FavoriteEvent.objects.filter(user=request.user)

    # Transform FavoriteEvent objects into the same format as search results
    processed_events = []
    for fav in favorite_events:
        processed_event = {
            'event_id': fav.event_id,
            'name': fav.event_name,
            'image': fav.event_image,
            'formatted_date': fav.event_date or "Date TBD",
            'formatted_time': fav.event_time or "Time TBD",
            'url': fav.event_url,
            'venue_name': fav.venue_name,
            'venue_address': fav.venue_address,
            'venue_city': fav.venue_city,
            'venue_state': fav.venue_state,
            'price_range': fav.price_range or "Price not available",
        }
        processed_events.append(processed_event)

    context = {
        'events': processed_events,
        'event_count': len(processed_events),
    }

    return render(request, 'favorites.html', context)

@login_required
def add_to_favorites(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        # Parse the JSON data from the request
        data = json.load(request)
        event = data.get('payload')

        # Try to create, but handle duplicate case
        favorite, created = FavoriteEvent.objects.get_or_create(
            user=request.user,
            event_id=event['event_id'],
            defaults={
                'event_name': event['name'],
                'event_url': event['url'],
                'event_image': event['image'],
                'event_date': event.get('formatted_date'),
                'event_time': event.get('formatted_time'),
                'venue_name': event['venue_name'],
                'venue_address': event['venue_address'],
                'venue_city': event['venue_city'],
                'venue_state': event['venue_state'],
                'price_range': event['price_range'],
            }
        )

        if created:
            return JsonResponse({'status': 'success', 'message': 'Added to favorites!'})
        else:
            return JsonResponse({'status': 'already_exists', 'message': 'Already favorited!'})
    else:
        return HttpResponseBadRequest('Invalid request')

@login_required
def remove_from_favorites(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        data = json.load(request)
        event = data.get('payload')

        FavoriteEvent.objects.filter(user=request.user, event_id=event['event_id']).delete()
        return JsonResponse({'status': 'success', 'message': 'Removed from favorites!'})

    else:
        return HttpResponseBadRequest('Invalid request')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form':form})

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
                    start_dates = event['dates']['start']

                    # Parse local date
                    local_date_str = start_dates.get('localDate')
                    if local_date_str:
                        local_date = datetime.strptime(local_date_str, '%Y-%m-%d')
                        formatted_date = local_date.strftime('%a, %b %d, %Y')
                    else:
                        formatted_date = "Date TBD"

                    # Parse local time
                    local_time_str = start_dates.get('localTime')
                    if local_time_str:
                        local_time = datetime.strptime(local_time_str, '%H:%M:%S')
                        formatted_time = local_time.strftime('%I:%M %p')
                    else:
                        formatted_time = "Time TBD"

                    # Extract price range if available
                    if 'priceRanges' in event and len(event['priceRanges']) > 0:
                        price_min = event['priceRanges'][0].get('min')
                        price_max = event['priceRanges'][0].get('max')

                        if price_min and price_max:
                            if price_min == price_max:
                                price_range = f"${price_min:.2f}"
                            else:
                                price_range = f"${price_min:.2f} - ${price_max:.2f}"
                        elif price_min:
                            price_range = f"From ${price_min:.2f}"
                        else:
                            price_range = "Price not available"
                    else:
                        price_range = "Price not available"

                    # Get the best quality image
                    best_image = get_best_quality_image(event.get('images', []))

                    # Create simplified event dictionary matching model and cartd fields
                    processed_event = {
                        'event_id': event['id'],
                        'name': event['name'],
                        'image': best_image,
                        'formatted_date': formatted_date,
                        'formatted_time': formatted_time,
                        'url': event['url'],
                        'venue_name': event['_embedded']['venues'][0]['name'],
                        'venue_address': event['_embedded']['venues'][0]['address']['line1'],
                        'venue_city': event['_embedded']['venues'][0]['city']['name'],
                        'venue_state': event['_embedded']['venues'][0]['state']['name'],
                        'price_range': price_range,
                    }

                    processed_events.append(processed_event)

                except (KeyError, IndexError, ValueError):
                    # Skip events with missing or invalid data
                    continue

    # Check which events are already favorited by the current user
    if request.user.is_authenticated:
        favorited_event_ids = set(
            FavoriteEvent.objects.filter(user=request.user).values_list('event_id', flat=True)
        )
        for event in processed_events:
            event['is_favorited'] = event['event_id'] in favorited_event_ids
    else:
        for event in processed_events:
            event['is_favorited'] = False

    # Create context dictionary with all data to pass to the template
    context = {
        'events': processed_events,
        'event_count': len(processed_events),
        'search_performed': search_performed,
    }

    # Render the template with context data
    return render(request, 'index.html', context)

def get_best_quality_image(images):
    """
    Select the highest quality image from a list of images based on dimensions.
    Returns the URL of the image with the largest width * height.
    If no images are available, returns None.
    """
    if not images:
        return None

    best_image = None
    max_area = 0

    for image in images:
        width = image.get('width', 0)
        height = image.get('height', 0)
        area = width * height

        if area > max_area:
            max_area = area
            best_image = image.get('url')

    return best_image if best_image else (images[0].get('url') if images else None)

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
