# @author Xavier Barneclo, Michael Jia
# weather API class

import socket
import requests

class Weather_API:

    # class instantiation by defining IPv6 address, api key, and other import variables
    def __init__(self):
        # get IPv6 address
        IPaddress = socket.getaddrinfo(socket.gethostname(), None, proto=socket.IPV6_PKTINFO)
        self.IPv6address = IPaddress[0][4][0]
        self.apiKey = "92108617754e4b78870099ac1ba1efdd"

        # definte theme lists
        SUNNY_LIST = ["Sunny", "Fair", "Sun", "Clear"]
        CLOUDY_LIST = ["Cloudy", "Overcast", "Clouds", "Mostly Cloudy", "Partly Cloudy", "Fog", "Haze", "Mist", "Smoke"]
        RAINY_LIST = ["Rainy", "Rain", "Thunderstorm", "Lightning", "Snow", "Hail", "Sleet", "Sprinkling", "Drizzling", "Raining"]
        self.THEME_LIST = [SUNNY_LIST,CLOUDY_LIST,RAINY_LIST]

    # gets longitude and latitude of IP location
    def IPGeolocation(self, IP) :
        # call api for IP location
        ipResponse = requests.get("https://api.ipgeolocation.io/ipgeo?apiKey=" + self.apiKey + "&" + str(IP))

        #grab the longitude and latitude from the json response
        latitude = ipResponse.json()["latitude"]
        longitude = ipResponse.json()["longitude"]
        return [latitude,longitude]

    # returns current weather of supplied coordinates
    def NWS(self, coordinates):
        latitude = coordinates[0]
        longitude = coordinates[1]

        #grab weather at location using weather api
        nwsResponse = requests.get("https://api.weather.gov/points/" + str(latitude) + "," + str(longitude))
        forecast = nwsResponse.json()["properties"]["forecastHourly"]
        nwsForecast = requests.get(forecast)

        forecastProperties = nwsForecast.json()["properties"]
        forecastPeriod = forecastProperties["periods"]
        todayweather = forecastPeriod[0]

        return todayweather

    # helper functions
    def theme_select(self, msg):
        for i in self.THEME_LIST:
            for q in i:
                if msg == q:
                    return i[0]

    # calls all functions and returns theme based on weather
    def get_theme(self):
        weather = self.NWS(self.IPGeolocation(self.IPv6address))["shortForecast"]
        return self.theme_select(weather)

