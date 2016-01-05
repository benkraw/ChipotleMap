import csv 
import pdb
import urllib, urllib2, json
import time 

def readData():
    data = []
    with open("chipotleLocations.csv", "rU") as f:
        reader = csv.reader(f)
        for row in reader:
            data.extend(row)
    return data 


def decode_address_to_coordinates(address):
    time.sleep(3)
    params = {
            'address' : address,
            'sensor' : 'false',
    }  
    url = 'http://maps.google.com/maps/api/geocode/json?' + urllib.urlencode(params)
    response = urllib2.urlopen(url)
    result = json.load(response)
    try:
            return result['results'][0]['geometry']['location']
    except:
            result = None

def main():
    data = readData()
    newData = []
    for adr in data:
        result = decode_address_to_coordinates(adr)
        print result 
        if result != None:
            result['addr'] = adr
            newData.append(result)

    with open('data.txt', 'w') as outfile:
        json.dump(newData, outfile)
main()