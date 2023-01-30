import requests
import json
import csv
import pandas as pd
import re

response_earthquake_25 = requests.get('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.geojson').text #2.5+ magnitude earthquakes
response_earthquake_45 = requests.get('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_month.geojson').text #4.5+ magnitude earthquakes
response_earthquake_sig = requests.get('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson').text #significant earthquakes

#take JSON string and make python dictionary using loads() method, doing this extra step to make new JSON with only relevant field for our exploration
earthquake_25_dict = json.loads(response_earthquake_25) 
earthquake_45_dict = json.loads(response_earthquake_45)
earthquake_sig_dict = json.loads(response_earthquake_sig)

# make dictionaries to later convert to "cleaned up" JSON and CSV. Lists contain all entries for given field
clean_dict_25 = {
                "place": [],
                "time": [],
                "mag": [],
                "felt": [],
                "alert": [],
                "tsunami": [],
                "coordinates": []
}

clean_dict_45 = {
                "place": [],
                "time": [],
                "mag": [],
                "felt": [],
                "alert": [],
                "tsunami": [],
                "coordinates": []
}

clean_dict_sig = {
                "place": [],
                "time": [],
                "mag": [],
                "felt": [],
                "alert": [],
                "tsunami": [],
                "coordinates": []
}


# populate dictionary 2.5+
key_set = {"place", "time", "mag", "felt", "alert", "tsunami"}

counter = 0
for i in earthquake_25_dict['features']:
    for key1 in i:
        if key1 == 'properties':
            for key2 ,value in earthquake_25_dict['features'][counter]['properties'].items():
                if key2 in key_set:
                    clean_dict_25[key2].append(value)
        if key1 == 'geometry':
            clean_dict_25["coordinates"].append(earthquake_25_dict['features'][counter]['geometry']['coordinates'])             
    counter+=1

# populate dictionary 4.5+
counter = 0
for i in earthquake_45_dict['features']:
    for key1 in i:
        if key1 == 'properties':
            for key2 ,value in earthquake_45_dict['features'][counter]['properties'].items():
                if key2 in key_set:
                    clean_dict_45[key2].append(value)               
        if key1 == 'geometry':
            clean_dict_45["coordinates"].append(earthquake_45_dict['features'][counter]['geometry']['coordinates'])   
    counter+=1

# populate dictionary significant
counter = 0
for i in earthquake_sig_dict['features']:
    for key1 in i:
        if key1 == 'properties':
            for key2 ,value in earthquake_sig_dict['features'][counter]['properties'].items():
                if key2 in key_set:
                    clean_dict_sig[key2].append(value)               
        if key1 == 'geometry':
            clean_dict_sig["coordinates"].append(earthquake_sig_dict['features'][counter]['geometry']['coordinates'])   
    counter+=1


#the way we we built the clean dict data structure, using pandas is the easiest choice for writing into CSV. If we had it formatted a different way we could have used the CSV DictWriter module. 
df25 = pd.DataFrame(clean_dict_25)
df25.to_csv('mag_2.5+.csv')

df45 = pd.DataFrame(clean_dict_45)
df45.to_csv('mag_4.5+.csv')

dfsig = pd.DataFrame(clean_dict_sig)
dfsig.to_csv('mag_sig+.csv')

# convert CSV to JSON
json25 = pd.read_csv('mag_2.5+.csv')
json25.to_json('mag_2.5+.json')

json45 = pd.read_csv('mag_4.5+.csv')
json45.to_json('mag_4.5+.json')

jsonsig = pd.read_csv('mag_sig+.csv')
jsonsig.to_json('mag_sig+.json')


#example of basic operation: print all location description of earthquakes that happened in Indonesia from newly created mag_2.5+ JSON

with open('mag_2.5+.json', 'r') as temp: 
    data = json.load(temp)

for key, value in data['place'].items():
        match = re.search(".* [I,i]ndonesia+.*", value)
        if match !=  None:
            print(match)