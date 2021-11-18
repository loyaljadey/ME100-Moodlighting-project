##This is the code for the test of how APis work and will be used for the subsequent setup of the IP location api
##source and reference off of https://www.dataquest.io/blog/python-api-tutorial/

##author: Michael Jia 
#         Mechanical Engineering 2024

##IMPORTS##

##must import requests in python via
##run the following command in the terminal
##windows: pip install requests
##linux: sudo pip install requests
import requests
##no need to install json or socket since it comes with python
import json
import socket



##INSTANCE VARIABLES##

##grabs the api address using the socket module that support IP requests
##https://docs.python.org/3/library/socket.html
##gets all the IPv6 addresses 
IPaddress = socket.getaddrinfo(socket.gethostname(), None, proto=socket.IPV6_PKTINFO)
#print(IPaddress)
##gets the specific wanted ipv6 address of the wifi router
##dictionary entry 1
##list entry 5
##dictionary entry 1
IPv6address = IPaddress[0][4][0]
#print(IPv6address)
#print(socket.has_ipv6)


##FUNCTIONS/METHODS##

##method for formatting the output of the api data that is outputted by the website
# param: obj
# type: object
# output: none 
# type: N/A
def jsonprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

##method for api access and geo positioning data return from the ipgeolocation.io website
##google login credentials
##vikksegal101@gmail.com
##limit 1000 calls a day 
##https://app.ipgeolocation.io/
# param: IP 
# type: str
# output: coordinates 
# type: []
apiKey = "92108617754e4b78870099ac1ba1efdd"
def IPGeolocation(IP) :
    ipResponse = requests.get("https://api.ipgeolocation.io/ipgeo?apiKey=" + apiKey + "&" + str(IP))
    #jsonprint(response2.json())

    ##grab the longitude and latitude from the json response
    ##response becomes a python dictionary
    ##["name of wanted output"]
    ##https://stackoverflow.com/questions/12788217/how-to-extract-a-single-value-from-json-response
    latitude = ipResponse.json()["latitude"]
    print(latitude)
    longitude = ipResponse.json()["longitude"]
    print(longitude)
    return [latitude,longitude]

##method for grabbing the National Weather Service API info
##https://www.weather.gov/documentation/services-web-api#
# param: coordinates 
# type: []
# output: weather
# type: {}
def NWS(coordinates):
    ##format input into latitude and longitude
    latitude = coordinates[0]
    longitude = coordinates[1]
    ##grab the gridpoints at the particular latitude and longitude
    nwsResponseGridPoints = requests.get("https://api.weather.gov/points/" + str(latitude) + "," + str(longitude))
    ##grab the properties of the response
    gridProperties = nwsResponseGridPoints.json()["properties"]
    ##these are the grid properties for the forecast of a particular area
    gridId = gridProperties["gridId"]
    gridX = gridProperties["gridX"]
    gridY = gridProperties["gridY"]

    nwsForecast = requests.get("https://api.weather.gov/gridpoints/" + str(gridId) + "/" + str(gridX) + "," + str(gridY) + "/forecast")
    forecastProperties = nwsForecast.json()["properties"]
    forecastPeriod = forecastProperties["periods"]
    todayweather = forecastPeriod[0]
    print(todayweather)

    return todayweather

##method to grab the temperature of the forecast
# param: weather
# type: {}
# output: temperature
# type: int
def temp(weather):
    #temperature from the weather api
    temperature = weather["temperature"]
    return temperature

##method to map temperature to color schemes in hexadecimal or in rgb values
##https://www.rapidtables.com/convert/color/rgb-to-hex.html
##https://htmlcolorcodes.com/colors/
# param: colorScheme, temp
# type: int, int
# output: gradient
# type: []
""" 
def tempGradient(colorscheme, temp):
    gradient = []
    if colorscheme == "warm":
        for x in range(10):
            gradient[x] = 
    elif colorscheme == "cold":
        for x in range(10):
            gradient[x] = 
    elif colorscheme == "retro":
        for x in range(10):
            gradient[x] = 
    elif colorscheme == "moody":
        for x in range(10):
            gradient[x] = 

245, 176, 65 
r = hex(255)
g = hex(255)
b = hex(255)
"0x" + r[len(r)-2] + r[len(r)-1] + g[len(g)-2] + g[len(g)-1] + b[len(b)-2] + b[len(b)-1]
"""
    


##RUNTIME EXECUTIONS##

##weather in F through the ipgeolocation api
print(str(temp(NWS(IPGeolocation(IPv6address)))) + ' F')
##forcast through a given coordinate
#print(NWS([37.8716,-122.2728]))


