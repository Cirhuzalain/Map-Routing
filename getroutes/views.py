import requests

from django.utils.html import escape
from django.http import JsonResponse
from django.db.models import Q
from getroutes.models import *
from getroutes.utils import *

def get_route_data(request):
    """
        Get route data by leveraging Google's Route API
        Return route in steps with navigation instruction and fuel location
    """
    try:
        routes_data = {"data" : [], "costs" : 0}
        start_location = escape(request.GET.get("start_location", "Boston, MA"))
        end_location = escape(request.GET.get("end_location", "San Fransisco, CA"))

        # get routes data from Google Routes API
        routes_response = get_routes([start_location, end_location])
        if routes_response.status_code != 200 :
            return JsonResponse(routes_data)

        routes_data["data"] = routes_response.json()
        
        # Save location but check first if location exist
        is_location = False
        location_filter = LocationRoute.objects.filter(start_location=start_location, end_location=end_location).first()

        if not location_filter:
            location_route_info = LocationRoute(start_location=start_location, end_location=end_location)
            location_route_info.save()
            is_location = True

        costs = 0
        travel_distance = 0
        final_routes_data = []

        for item in routes_data["data"]["routes"][0]["legs"][0]["steps"]:
            distance_miles = (item["distanceMeters"]/1000)*0.621371
            travel_distance += distance_miles

            # Save route data 
            start_lat, start_lng = item["startLocation"]["latLng"]["latitude"], item["startLocation"]["latLng"]["longitude"]
            start_location_info = f"{start_lat}, {start_lng}"

            end_lat, end_lng = item["endLocation"]["latLng"]["latitude"], item["endLocation"]["latLng"]["longitude"]
            end_location_info = f"{start_lat}, {start_lng}"

            instruction_info, maneuver_info= "", ""

            if "navigationInstruction" in item:
                instruction_info = item["navigationInstruction"]["instructions"]
                maneuver_info = item["navigationInstruction"]["maneuver"]

            if len(instruction_info) > 300:
                instruction_info = instruction_info[:300]

            item_data = {
                "distance" : item["distanceMeters"],
                "start_location" : start_location_info,
                "end_location" : end_location_info,
                "maneuver" : maneuver_info,
                "instructions" : instruction_info,
                "travelMode" : item["travelMode"],
            }
            
            if is_location:
                route_info = Routes(distance=item_data["distance"], \
                                    start_location_latlng=item_data["start_location"], \
                                    end_location_latlng=item_data["end_location"], \
                                    maneuver=item_data["maneuver"], \
                                    instructions=item_data["instructions"],
                                    travelMode=item_data["travelMode"], \
                                    location_route=location_route_info)
                route_info.save()
            final_routes_data.append(item_data)
            
            # Add location fo fuel after 400 miles
            if travel_distance >= 400:
                current_latlng = item["endLocation"]["latLng"]
                lat, lng = current_latlng["latitude"], current_latlng["longitude"]
                location_info = f"{lat}, {lng}"

                location = get_location_details(location_info)
                if location:
                    city, state = "", ""
                    if "city" in location.raw["address"]:
                        city = location.raw["address"]["city"]
                    if "state" in location.raw["address"]:
                        state = location.raw["address"]["state"]

                    state_code = get_state_code(state)
                    location_price_info = LocationPrice.objects.filter(Q(city__icontains=city) | Q(state__icontains=state_code))

                    if location_price_info:
                        min_price = float("inf")
                        min_location = None
                        for loc in location_price_info:
                            if loc.retail_price < min_price:
                                min_location = loc
                                min_price = loc.retail_price
                        
                        # calculate costs and add location to fuel
                        total_distance_miles = (routes_data["data"]["routes"][0]["distanceMeters"]/1000)*0.621371
                        costs = float(min_location.retail_price)*(total_distance_miles/10)
                        price_info_data = {
                            "truck_stop_id" : min_location.truck_stop_id,
                            "truck_stop_name" : min_location.truck_stop_name,
                            "address" : min_location.address,
                            "city" : min_location.city,
                            "state" : min_location.state,
                            "rack_id" : min_location.rack_id,
                            "retail_price": min_location.retail_price,
                        }
                        final_routes_data.append(price_info_data)

                travel_distance = 0

        routes_data["data"] = final_routes_data
        routes_data["costs"] = costs

        return JsonResponse(routes_data)
    except Exception as e:
        return JsonResponse({"error" : str(e)}, status=500)