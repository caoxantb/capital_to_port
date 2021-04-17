import pandas as pd 
import json
import math
import sys

class Capital:
    ##Constructor
    def __init__(self, name, country, lat, lng, dist):
        self.name = name
        self.country = country
        self.lat = lat
        self.lng = lng
        self.dist = dist
    
    def calc_distance(self, port_lat, port_lng):
        R = 6371
        DEG_TO_RAD = math.pi/180
        h = (1 - math.cos((port_lat - self.lat)*DEG_TO_RAD))/2 + math.cos(self.lat*DEG_TO_RAD)*math.cos(port_lat*DEG_TO_RAD)*(1 - math.cos((port_lng - self.lng)*DEG_TO_RAD))/2
        d = 2*R*math.asin(math.sqrt(h))

        return d

if __name__ == '__main__':
    ## Read cities.csv
    capitals = []

    cities_df = pd.read_csv("cities.csv", encoding="utf-8-sig")

    for i in range(len(cities_df)):
        if cities_df.loc[i, "capital"] == "primary":
            capitals.append(
                Capital(
                    cities_df.loc[i, "city"], 
                    cities_df.loc[i, "country"], 
                    cities_df.loc[i, "lat"], 
                    cities_df.loc[i, "lng"],
                    0
                )
            )

    ## Read ports.json
    ports = []

    with open("ports.json") as f:
        ports_json = json.load(f)

    for port in ports_json["features"]:
        if port["properties"]["prttype"] == "Sea":
            ports.append(
                {
                    "lat": port["properties"]["latitude"],
                    "lng": port["properties"]["longitude"]
                }
            )

    ## Find shortest distance
    data = {"country": [], "capital": [], "shortest_dist_in_kms": []} 

    for capital in capitals:
        min_d = sys.maxsize
        for port in ports:
            d = capital.calc_distance(port["lat"], port["lng"])
            if d <= min_d: min_d = d
        capital.dist = round(min_d, 4)

        data["country"].append(capital.country)
        data["capital"].append(capital.name)
        data["shortest_dist_in_kms"].append(capital.dist)
    
    # Return result as .csv file
    df = pd.DataFrame(data)
    df.to_csv(r"result.csv", index=False, header=True, encoding="utf-8-sig")
    