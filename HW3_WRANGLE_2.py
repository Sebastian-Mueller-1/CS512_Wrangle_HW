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
df25.to_csv('mag_2.5+.csv', index=False, na_rep="Null")

df45 = pd.DataFrame(clean_dict_45)
df45.to_csv('mag_4.5+.csv', index=False, na_rep="Null" )

dfsig = pd.DataFrame(clean_dict_sig)
dfsig.to_csv('mag_sig+.csv',index=False, na_rep="Null")

# convert CSV to JSON
json25 = pd.read_csv('mag_2.5+.csv', encoding='utf-8')
json25.to_json('mag_2.5+.json',indent = 1, orient='records',force_ascii=False)

json45 = pd.read_csv('mag_4.5+.csv', encoding='utf-8')
json45.to_json('mag_4.5+.json',indent = 1, orient='records',force_ascii=False)

jsonsig = pd.read_csv('mag_sig+.csv', encoding='utf-8')
jsonsig.to_json('mag_sig+.json',indent = 1, orient='records',force_ascii=False)

# manually prepend outer object for each JSON for correct formatting
prepend = '{\n"2.5+_earthquake_records":'
with open("mag_2.5+.json", 'r+') as temp: 
    temp_data = temp.read()
    temp.seek(0,0)
    temp.write(prepend+'\n'+temp_data)
    temp.seek(0,2) # send pointer to end of file
    temp.write('\n'+"}") # add closing dictionary bracket
temp.close()

prepend = '{\n"4.5+_earthquake_records":'
with open("mag_4.5+.json", 'r+') as temp: 
    temp_data = temp.read()
    temp.seek(0,0)
    temp.write(prepend+'\n'+temp_data)
    temp.seek(0,2) # send pointer to end of file
    temp.write('\n'+"}") # add closing dictionary bracket
temp.close()


prepend = '{\n"significant_earthquake_records":'
with open("mag_sig+.json", 'r+') as temp: 
    temp_data = temp.read()
    temp.seek(0,0)
    temp.write(prepend+'\n'+temp_data)
    temp.seek(0,2) # send pointer to end of file
    temp.write('\n'+"}") # add closing dictionary bracket
temp.close()

# example of basic operation: print all location description of earthquakes that happened in Indonesia from newly created mag_2.5+ JSON

with open('mag_2.5+.json', 'r') as temp: 
    data = json.load(temp)

for i in data['2.5+_earthquake_records']:
    for key, value in i.items():
        if key == 'place':
            match = re.search(".* [I,i]ndonesia+.*", value)
            if match !=  None:
                print(match)

