import requests
import json
import random
import math

def get_nearby_petrol_pumps(source, radius, api_key):
    # Define the Places API endpoint
    places_endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    # Define parameters for Places API request
    params = {
        "location": source,
        "radius": radius,
        "keyword": "petrol pump",
        "key": "AIzaSyAI1kcUukYd6Md_1y88KauY9tLYpqRbvMw"
    }

    # Make the Places API request
    response = requests.get(places_endpoint, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        return data.get("results", [])
    else:
        print("Error:", response.status_code)
        return []

def get_distance_matrix(origins, destinations, api_key):
    # Define the Distance Matrix API endpoint
    endpoint = "https://maps.googleapis.com/maps/api/distancematrix/json"

    # Define parameters for Distance Matrix API request
    params = {
        "origins": origins,
        "destinations": destinations,
        "key": "AIzaSyAI1kcUukYd6Md_1y88KauY9tLYpqRbvMw"
    }

    # Make the Distance Matrix API request
    response = requests.get(endpoint, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        return data.get("rows", [])
    else:
        print("Error:", response.status_code)
        return []


def get_route(source, destination, api_key):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={source}&destination={destination}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        route = data['routes'][0]['legs'][0]['steps']
        return route
    else:
        print("Error:", data['status'])
        return None

def get_points_along_route(route, interval_distance):
    points = []
    initial_lat = 21.125612
    initial_lng = 79.052092
    # points.append((initial_lat,initial_lng))
    distance_covered = 0.0
    for step in route:
        lat_start = step['start_location']['lat']
        lng_start = step['start_location']['lng']
        lat_end = step['end_location']['lat']
        lng_end = step['end_location']['lng']
        step_distance = float(step['distance']['value']) / 1000.0  # convert to km
        while distance_covered + step_distance >= interval_distance:
            remaining_distance = interval_distance - distance_covered
            ratio = remaining_distance / step_distance
            lat = lat_start + (lat_end - lat_start) * ratio
            lng = lng_start + (lng_end - lng_start) * ratio
            points.append((lat, lng))
            step_distance -= remaining_distance
            distance_covered = 0.0
        distance_covered += step_distance
    return points

def main():
    initial_source = "21.125612, 79.052092"  # Replace with your source address or coordinates
    destination = "WQH4+VP9, Amrawati Tahsil, Amravati, Maharashtra 444601"  # Replace with your destination address or coordinates
    api_key = ""  # Replace with your Google API key
    
    # initial_charge in KWH
    initial_charge = 20.0
    # final capacity in KWhr
    max_capacity = 60.0
    # maximum percetage allowed 
    beta = 0.80
    final_charge = max_capacity * beta
    # kwhr consumed per 100 km
    alpha = 15.0
    # in kWhr/hr = Kw
    # rate_of_charge = 15.0

    max_radius = (100*initial_charge)/alpha 
    actual_distance = max_radius*0.90
    # 0.9 is due to weather / uphill

   
    total_distance = get_distance_matrix(initial_source, destination, api_key)
    with open('dumpster_distances.json', 'w') as file:
                json.dump(total_distance, file, indent=4)
    total_distance_value = (total_distance[0]['elements'][0]['distance']['value']/1000) 

    if(actual_distance >= total_distance_value):
        print("No petrol pump needed");
        print("src_to_destination time - " + str(ceil(total_distance[0]['elements'][0]['duration']['value']/60)) + " min")
    else : 
        # array of sources
        source = []
        source.append(initial_source)
        # print(type(source))
        
        interval_distance = 10  # in kilometers
        distance_api_key = "AIzaSyCD6DDnaCijGSwWIip54Dnlyk1KL77OEow"
        route = get_route(initial_source, destination, distance_api_key)
        if route:
            points = get_points_along_route(route, interval_distance)
            # print(type(points))
            print("Points along the route (after traveling 10 km intervals):")
            for point in points:
                print(point)

            if(actual_distance > 10):
                value = int(actual_distance/10) 
                print(value)
                i = 0
                while(value):
                    
                    source.append(points[i])
                    i = i + 1
                    value = value - 1

            for sources in source:
                print(sources)
        else:    
            print("Error getting route.")


        #   actual_distance in km

        original_src_new_src_distances = []
        original_src_new_src_duration = []
        initial_charge = 20.0
        # KWH

        new_distance = []
        initial_lat = 21.125612
        initial_lng = 79.052092
        # Get distances from source to petrol pumps and from petrol pumps to destination
        distances = []
        for sources in source : 
            
            sources1 = ",".join(str(item) for item in sources)
          

            circle_radius = min(actual_distance,10)
            circle_radius = circle_radius*1000  # m radius for finding petrol pumps
           
            # initial_charge1 = initial_charge - (alpha/100) * total_distance_value

            petrol_pumps = get_nearby_petrol_pumps(sources1, circle_radius, api_key)

          

            source_to_pump_distances = []
            pump_to_destination_distances = []

        
            # j = 0;
            queue_time = []
            charge_rate = []

            for pump in petrol_pumps:
                petrol_pump_coords = f"{pump['geometry']['location']['lat']},{pump['geometry']['location']['lng']}"
                source_to_pump = get_distance_matrix(initial_source, petrol_pump_coords, api_key)
                pump_to_destination = get_distance_matrix(petrol_pump_coords, destination, api_key)
                       
                # 0.9 is due to weather / uphill
                if(pump_to_destination[0]['elements'][0]['distance']['value']/1000 > (100*final_charge)*0.9/alpha):
                    continue

                # queue time 
                q_random_number = random.randint(30, 120)
                c_random_number = random.randint(15,20)
                queue_time.append(q_random_number)
                charge_rate.append(c_random_number)
                q_random_number -= source_to_pump[0]['elements'][0]['duration']['value']/60

                charge_time = (final_charge - (initial_charge - (alpha/100) * source_to_pump[0]['elements'][0]['distance']['value']/1000))/c_random_number
                # in minutes
                charge_time = charge_time * 60

                # j = j + 1;
                # if(j == 1):
                #     print(source_to_pump)
                #     print(pump_to_destination)
                distances.append({
                    "petrol_pump_name": pump["name"],
                    "petrol_pump_coords": str(f"{pump['geometry']['location']['lat']},{pump['geometry']['location']['lng']}"),
                    "original_source_to_pump_distance": str(source_to_pump[0]['elements'][0]['distance']['value']/1000) + "km",
                    "original_source_to_pump_duration": str(source_to_pump[0]['elements'][0]['duration']['value']/60) + "min",
                    "pump_to_destination_distance": str(pump_to_destination[0]['elements'][0]['distance']['value']/1000) + "km",
                    "pump_to_destination_duration": str(pump_to_destination[0]['elements'][0]['duration']['value']/60) + "min",
                    "total_time" : str(source_to_pump[0]['elements'][0]['duration']['value']/60 + max(0,q_random_number) + pump_to_destination[0]['elements'][0]['duration']['value']/60 + 
                    + charge_time) + " minutes"
                })
            actual_distance -= 10 

        if(len(distances) != 0):

            #sort distance here 
            sorted_distances = sorted(distances, key=lambda x: x["total_time"])
            print("Sorted distances array:")
            for distance in sorted_distances:
                print(distance)

            # Save distances to JSON file 
            with open('petrol_pump_distances' + str(i) + '.json', 'w') as file:
                json.dump(sorted_distances, file, indent=4)
            print("Petrol pump distances saved to petrol_pump_distances.json")
        else:
            print("Not possible with single petrol pump!")
            # Code here


if __name__ == "__main__":
    main()
