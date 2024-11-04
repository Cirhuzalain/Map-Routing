def read_data():
    with open("getroutes/fuel-prices-for-be-assessment.csv") as file:
        location_reader = csv.reader(file)
        for row in location_reader:
            if  row[1] not in data_locations:
                data.append(row)
                data_locations.append(row[1])
            
    with open("getroutes/fuel_final.csv", "w") as file:
        location_writer = csv.writer(file)
        for row in data:
            location_writer.writerow(row)
    # routes_data["data"] = data
    routes_data["length"] = len(data_locations)

def save_data():
    data = []
    with open("getroutes/fuel_final.csv") as file:
    location_reader = csv.reader(file)
    next(location_reader, None)
    for row in location_reader:
        # save row to the db
        location_price = LocationPrice(truck_stop_id=int(row[0]), truck_stop_name=row[1].strip(), \
                                                 address=row[2].strip(), city=row[3].strip(), state=row[4].strip(), \
                                                 rack_id=int(row[5]), retail_price=float(row[6]))
        location_price.save()

def load_json_data():
    with open("getroutes/data.json") as f:
        d = json.load(f)
        routes_data["length"] = len(d["data"]["routes"][0]["legs"][0]["steps"])
        routes_data["data"] = d["data"]