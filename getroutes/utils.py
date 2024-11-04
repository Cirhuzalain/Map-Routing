import requests
import os
from geopy.geocoders import Nominatim

def get_routes(locations):
    """
        Get routes details
    """
    body = {
        "origin": {
            "address": locations[0]
        },
        "destination": {
            "address": locations[1]
        },
        "travelMode": "DRIVE"
    }
    api_key = os.environ.get("G_API_KEY", "")
    headers = {"Content-Type": "application/json", "X-Goog-Api-Key" : api_key, \
                "X-Goog-FieldMask" : "routes.duration,routes.distanceMeters,routes.legs.steps"}

    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    response = requests.post(url, headers=headers, json=body)

    return response

def get_location_details(latlng):
    """
        Get location details
    """
    geolocator = Nominatim(user_agent="Test Routing")
    location = geolocator.reverse(latlng)
    return location

def get_state_code(state_name):
    """
        Get state code
    """
    statename_data = {
            'District of Columbia': 'DC',
            'Alabama': 'AL',
            'Montana': 'MT',
            'Alaska': 'AK',
            'Nebraska': 'NE',
            'Arizona': 'AZ',
            'Nevada': 'NV',
            'Arkansas': 'AR',
            'New Hampshire': 'NH',
            'California': 'CA',
            'New Jersey': 'NJ',
            'Colorado': 'CO',
            'New Mexico': 'NM',
            'Connecticut': 'CT',
            'New York': 'NY',
            'Delaware': 'DE',
            'North Carolina': 'NC',
            'Florida': 'FL',
            'North Dakota': 'ND',
            'Georgia': 'GA',
            'Ohio': 'OH',
            'Hawaii': 'HI',
            'Oklahoma': 'OK',
            'Idaho': 'ID',
            'Oregon': 'OR',
            'Illinois': 'IL',
            'Pennsylvania': 'PA',
            'Indiana': 'IN',
            'Rhode Island': 'RI',
            'Iowa': 'IA',
            'South Carolina': 'SC',
            'Kansas': 'KS',
            'South Dakota': 'SD',
            'Kentucky': 'KY',
            'Tennessee': 'TN',
            'Louisiana': 'LA',
            'Texas': 'TX',
            'Maine': 'ME',
            'Utah': 'UT',
            'Maryland': 'MD',
            'Vermont': 'VT',
            'Massachusetts': 'MA',
            'Virginia': 'VA',
            'Michigan': 'MI',
            'Washington': 'WA',
            'Minnesota': 'MN',
            'West Virginia': 'WV',
            'Mississippi': 'MS',
            'Wisconsin': 'WI',
            'Missouri': 'MO',
            'Wyoming': 'WY',
    }
    return statename_data[state_name]