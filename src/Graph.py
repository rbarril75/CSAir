'''
Created on Sep 26, 2011

@author: Ryan
'''

import simplejson #@UnresolvedImport
import urllib
import sys
import Airport
import City
import Flight
import Queue
import math
import webbrowser

class graph():

    ''' Initialize graph data structures '''
    def __init__(self):
        self.airportDictionary = dict() # Maps airport codes to airport objects
        self.cityDictionary = dict() # Maps city names to city objects 
        self.flightDictionary = dict() # Maps flight route codes to flight objects
        self.populateDatabase('map_data.json') # Populate dictionaries
    
    ''' Populates data structures by extracting and transferring information from a JSON file '''
    def populateDatabase(self, JSONFileName):
        try:
            rawDataDictionary = simplejson.load(urllib.urlopen(JSONFileName))
        except:
            print("Invalid JSON file name")
            return
        metroList = rawDataDictionary.get('metros')
        routeList = rawDataDictionary.get('routes')
        self.initializeCities(metroList)
        self.initializeRoutes(routeList)

    ''' Extracts and adds data from a dictionary of city information '''
    def initializeCities(self, metroList):
        for metro in metroList:
            code = str(metro.get('code'))
            cityName = str(metro.get('name'))
            country = str(metro.get('country'))
            continent = str(metro.get('continent'))
            timezone = metro.get('timezone')
            coordinates = metro.get('coordinates')
            population = metro.get('population')
            region = metro.get('region')
            
            self.addCity(cityName, country, continent, timezone, coordinates, population, region, code)
   
    ''' Extracts and adds data from a dictionary of flight information '''    
    def initializeRoutes(self, routeList):
        for route in routeList:
                routePorts = route.get('ports')
                code1 = routePorts[0]
                code2 = routePorts[1]
                flightDistance = route.get('distance')
                                                
                airport1 = self.getAirport(code1)
                airport2 = self.getAirport(code2)  

                self.addRoute(airport1, airport2, flightDistance)
                
    def addJSON(self):
        print("Enter name of JSON file: "),
        fileName = raw_input()
        self.populateDatabase(fileName)

    ''' Returns airport object associated with parameter airport code '''   
    def getAirport(self, code):
        try:
            return self.airportDictionary[code]
        except:
            print("Invalid airport code.")
            return None
        
    ''' Returns flight object associated with parameter flight route code '''   
    def getFlight(self, routeCode):
        try:
            return self.flightDictionary[routeCode]
        except:
            print("Invalid route code.")
            return None
        
    ''' Returns city object associated with parameter cityc name '''   
    def getCity(self, cityName):
        try:
            return self.cityDictionary[cityName]
        except:
            print("Invalid city name.")
            return None  
    
    ''' Lists every city in the database '''      
    def listCities(self):
        print("CSAir SERVES THESE CITIES:")

        citiesPerLineLimit = 10
        cityNumber = 1
        
        cityIterator = self.cityDictionary.itervalues()
        while True:
            try:
                city = cityIterator.next()
            except StopIteration:
                break
            
            if (cityNumber > citiesPerLineLimit):
                print("")
                cityNumber = 1
            
            print(city.getName() + ";"),
            cityNumber += 1            
                
        print("")
                                
    def requestCityInput(self):
        print("Enter a city's name:"),
        cityQuery = raw_input()
        print("")
        
        cityIterator = self.cityDictionary.itervalues()
        while True:
            try:
                city = cityIterator.next()
            except StopIteration:
                break
            
            cityName = city.getName()
            if cityName == cityQuery:
                self.listAttributes(city)
                return
            
        print("City not found")
            
    ''' Lists every attribute of a parameter city '''
    def listAttributes(self, city):        
        print("CITY STATISTICS FOR " + city.getName())
        print("Country: " + city.getCountry())
        print("Continent: " + city.getContinent())
        print("Time Zone: " + str(city.getTimezone()))
        print("Latitude/Longitude: " + city.getCoordinates())
        print("Population: " + str(city.getPopulation()))
        print("Region: " + str(city.getRegion()))
        print("Airport Code: " + city.getAirportCode())
        
        airport = self.getAirport(city.getAirportCode())
        airport.printFlights()
    
    def requestStatsInput(self):
        print("(1) Print All Statistics")
        print("(2) Print Shortest Flight")
        print("(3) Print Longest Flight")
        print("(4) Print Average Flight Length")
        print("(5) Print Smallest City")
        print("(6) Print Largest City")
        print("(7) Print Average City Population")
        print("(8) Print All Cities by Continent")
        print("(9) Print Hub Cities")
        print("Enter a command:"),
        
        statsQuery = raw_input()
        print("")
        
        if (statsQuery == "1"):
            self.printAllStats()
        elif (statsQuery == "2"):
            self.printShortestFlight()
        elif (statsQuery == "3"):
            self.printLongestFlight()
        elif (statsQuery == "4"):
            self.printAverageFlightLength()
        elif (statsQuery == "5"):
            self.printSmallestCity()
        elif (statsQuery == "6"):
            self.printLargestCity()
        elif (statsQuery == "7"):
            self.printAverageCityPopulation()
        elif (statsQuery == "8"):
            self.printContinentStats()
        elif (statsQuery == "9"):
            self.printHubCities()
        else:
            print("Invalid command.")
            
    def printAllStats(self):
        print("CSAir STATISTICS")
        print("")
        self.printFlightLengthStats()
        print("")
        self.printPopulationStats()
        print("")
        self.printContinentStats()
        print("")
        self.printHubCities()

    ''' Prints statistics of the shortest and longest flights '''
    def printFlightLengthStats(self):
        print("FLIGHT DISTANCE STATISTICS")
        self.printShortestFlight()
        self.printLongestFlight()
        print("Average Flight Length: " + str(self.getAverageFlightLength()) + "km")
     
    ''' Returns shortest flight, by distance, in the database '''   
    def getShortestFlight(self):
        shortestLength = -1
        
        flightIterator = self.flightDictionary.itervalues()
        while True:
            try:
                flight = flightIterator.next()
            except StopIteration:
                break
            
            flightDistance = flight.getDistance()
            
            if (shortestLength == -1 or 
                flightDistance < shortestLength):
                shortestLength = flightDistance
                shortestFlight = flight
        
        return shortestFlight
    
    def printShortestFlight(self):
        shortestFlight = self.getShortestFlight()
        print("Shortest Flight: " + shortestFlight.getItinerary())
    
    ''' Returns longest flight, by distance, in the database '''    
    def getLongestFlight(self):
        longestLength = -1
        
        flightIterator = self.flightDictionary.itervalues()
        while True:
            try:
                flight = flightIterator.next()
            except StopIteration:
                break
            
            flightDistance = flight.getDistance()
            
            if (longestLength == -1 or
                flightDistance > longestLength):
                longestLength = flightDistance
                longestFlight = flight
                
        return longestFlight
    
    def printLongestFlight(self):
        longestFlight = self.getLongestFlight()        
        print("Longest Flight: " + longestFlight.getItinerary())

    ''' Computes and returns the average length of all flights '''
    def getAverageFlightLength(self):
        flightSum = 0
        
        flightIterator = self.flightDictionary.itervalues()
        while True:
            try:
                flight = flightIterator.next()
            except StopIteration:
                break
            
            flightDistance = flight.getDistance()                
            flightSum += flightDistance
            
        averageFlightLength = flightSum / self.getFlightCount()
        return averageFlightLength
    
    def printAverageFlightLength(self):
        averageFlightLength = self.getAverageFlightLength()
        print("Average Flight Length: " + str(averageFlightLength) + "km")
    
    def getFlightCount(self):
        return len(self.flightDictionary)
        
    def printPopulationStats(self):
        print("CITY POPULATION STATISTICS")
        self.printSmallestCity()
        self.printLargestCity()
        self.printAverageCityPopulation()
    
    ''' Returns the smallest city, by population, in the database ''' 
    def getSmallestCity(self):
        smallestPopulation = -1
        
        cityIterator = self.cityDictionary.itervalues()
        while True:
            try:
                city = cityIterator.next()
            except StopIteration:
                break
            
            cityPopulation = city.getPopulation()
            
            if (smallestPopulation == -1 or 
                cityPopulation < smallestPopulation):
                smallestPopulation = cityPopulation
                smallestCity = city
        
        return smallestCity
        
    def printSmallestCity(self):
        smallestCity = self.getSmallestCity()
        print("Smallest City by Population: " + smallestCity.getName() + ", " + str(smallestCity.getPopulation()) + " people")

    ''' Returns largest city, by population, in the database '''   
    def getLargestCity(self):
        largestPopulation = -1
        
        cityIterator = self.cityDictionary.itervalues()
        while True:
            try:
                city = cityIterator.next()
            except StopIteration:
                break
            
            cityPopulation = city.getPopulation()
            
            if (largestPopulation == -1 or 
                cityPopulation > largestPopulation):
                largestPopulation = cityPopulation
                largestCity = city     
                
        return largestCity
    
    def printLargestCity(self):
        largestCity = self.getLargestCity()
        print("Largest City by Population: " + largestCity.getName() + ", " + str(largestCity.getPopulation()) + " people")
 
    ''' Computes and returns the average population of all cities '''
    def getAverageCityPopulation(self):        
        populationSum = 0
        
        cityIterator = self.cityDictionary.itervalues()
        while True:
            try:
                city = cityIterator.next()
            except StopIteration:
                break
            cityPopulation = city.getPopulation()                
            populationSum += cityPopulation
            
        averageCityPopulation = populationSum / self.getCityCount()
        
        return averageCityPopulation
    
    def printAverageCityPopulation(self):
        averageCityPopulation = self.getAverageCityPopulation()
        print("Average City Population: " + str(averageCityPopulation) + " people")
    
    def getCityCount(self):
        return len(self.cityDictionary)
    
    def printContinentStats(self):
        print("CITIES BY CONTINENT")
        self.printCitiesIn("North America")
        print("")
        self.printCitiesIn("South America")
        print("")
        self.printCitiesIn("Africa")
        print("")
        self.printCitiesIn("Europe")
        print("")
        self.printCitiesIn("Asia")
        print("")
        self.printCitiesIn("Australia")
        print("")
    
    ''' Prints every city in a given parameter continent ''' 
    def printCitiesIn(self, continentInput):
        outputList = []
        
        cityIterator = self.cityDictionary.itervalues()
        while True:
            try:
                city = cityIterator.next()
            except StopIteration:
                break
            
            cityName = city.getName()            
            continentName = city.getContinent()
            
            if (continentName == continentInput):
                outputList.append(cityName)
        
        self.printCityList("Cities in " + continentInput + ":", outputList)
    
    def printCityList(self, listName, cityList):
        print(listName),
        for cityName in cityList:
            print(cityName + ";"),
    
    ''' Returns a list of hub cities, defined as cities with at least 5 connections '''
    def getHubCities(self):
        airportIterator = self.airportDictionary.itervalues()
        hubCities = []
        
        while True:
            try:
                airport = airportIterator.next()
            except StopIteration:
                break
            
            flights = airport.getFlights()
            connectionsCount = len(flights)
            if (connectionsCount >= 5):
                city = airport.getCity()
                cityName = city.getName()
                hubCities.append(cityName)
                
        return hubCities
    
    def printHubCities(self): 
        hubCities = self.getHubCities() 
        
        print("HUB CITIES (5+ CONNECTIONS)")
        self.printCityList("Hub Cities:", hubCities)
        print("")
    
    def getMapURL(self):
        mapURL = "http://www.gcmap.com/mapui?P="
        firstFlightSet = -1
        
        flightIterator = self.flightDictionary.itervalues()
        while True:
            try:
                flight = flightIterator.next()
            except StopIteration:
                break
            
            if (firstFlightSet == -1):
                firstRouteCode = flight.getRouteCode()
                mapURL += firstRouteCode
                firstFlightSet = 0
            else:
                mapURL += ",+" + flight.getRouteCode()
                
        return mapURL
    
    ''' Displays each flight in gcmap.com '''
    def printMapURL(self):
        mapURL = self.getMapURL()      
        print("MAP URL: " + mapURL)
        webbrowser.open_new(mapURL)
    
    def editGraph(self):
        
        print("Enter password (case-sensitive): "),
        password = raw_input()
        
        if (password == "illini"):
            pass
        else:
            print("Password is incorrect.")
            return
        
        print("")        
        print("ACTIONS")
        print("(1) Remove a City")
        print("(2) Remove a Route")
        print("(3) Add a City")
        print("(4) Add a Route")
        print("(5) Edit a City")
        print("Enter a command:"),
        
        editQuery = raw_input()
        print("")
        
        if (editQuery == "1"):
            self.requestCityToRemove()
        elif (editQuery == "2"):
            self.requestRouteToRemove()
        elif (editQuery == "3"):
            self.requestCityInfo()
        elif (editQuery == "4"):
            self.requestRouteInfo()
        elif (editQuery == "5"):
            self.requestEditInfo()
        else:
            print("Invalid command.")
    
    def requestCityToRemove(self):
        print("Enter a city to remove: "),
        cityName = raw_input()
        cityToRemove = self.getCity(cityName)
        if (cityToRemove == None):
            return
    
        self.removeCity(cityToRemove)
    
    ''' Deletes a city and all its references from the database '''
    def removeCity(self, cityToRemove):
        airportCode = cityToRemove.getAirportCode()
        airportToRemove = self.getAirport(airportCode)
        
        self.removeFlightsInvolving(airportToRemove)
        del self.airportDictionary[airportCode]
        del self.cityDictionary[cityToRemove.getName()]
    
    ''' Deletes the flights of a given airport, presumably one that is to be rmeoved '''
    def removeFlightsInvolving(self, airport):
        flightsToRemove = airport.getListOfFlights()
        
        for flight in flightsToRemove[:]:
            returnFlight = self.getReturnFlight(flight)
            self.deleteFromDatabase(flight)
            self.deleteFromDatabase(returnFlight)
    
    ''' Returns the flight going in the opposite direction of the parameter flight '''
    def getReturnFlight(self, flight):
        routeCode = flight.getRouteCode()
        returnRouteCode = routeCode[4:] + "-" + routeCode[0:3] #[4:] specifies second airport code. [0:3] specifies first.
        returnFlight = self.getFlight(returnRouteCode)
        return returnFlight
    
    ''' Remove's a flight's references in the database '''
    def deleteFromDatabase(self, flightToRemove):
        departurePort = flightToRemove.getDeparturePort()
        departurePort.removeFlight(flightToRemove)
            
        routeCode = flightToRemove.getRouteCode()
        del self.flightDictionary[routeCode]
        
    def requestRouteToRemove(self):
        print("Enter a route to remove (use form AAA-BBB): "),
        routeCode = raw_input()
        
        self.removeRoute(routeCode)
    
    ''' Remove's a flight, and it's corresponding return flight, from the database '''
    def removeRoute(self, routeCode):
        flightToRemove = self.getFlight(routeCode)
        if (flightToRemove == None):
            return

        returnFlightToRemove = self.getReturnFlight(flightToRemove)
        
        self.deleteFromDatabase(flightToRemove)
        self.deleteFromDatabase(returnFlightToRemove)
    
    def requestCityInfo(self):
        print("Enter city name: "),
        name = raw_input()
        print("Enter country: "),
        country = raw_input()
        print("Enter continent: "),
        continent = raw_input()
        print("Enter timezone: "),
        try: timezone = int(raw_input())
        except:
            print("Invalid timezone.")
            return
        print("Enter latitude (form \"DIR #\"): "),
        latitude = raw_input()
        print("Enter longitude(form \"DIR #\"): "),
        longitude = raw_input()
        print("Enter population: "),
        try: population = int(raw_input())
        except:
            print("Invalid population.")
            return
        print("Enter region: "),
        try: region = int(raw_input())
        except:
            print("Invalid region")
            return
        print("Enter airport code: "),
        code = raw_input() 
    
        coordinates = self.parseCoordinates(latitude, longitude)
        self.addCity(name, country, continent, timezone, coordinates, population, region, code)
    
    ''' Creates a new city ''' 
    def addCity(self, name, country, continent, timezone, coordinates, population, region, code):      
        newCity = City.city(name, country, continent, timezone, coordinates, population, region, code)
        newAirport = Airport.airport(code, newCity, dict())
        self.cityDictionary[name] = newCity
        self.airportDictionary[code] = newAirport
    
    ''' Given a latitude and longitude strings, formats them into a dictionary '''
    def parseCoordinates(self, latitude, longitude):
        latDir = latitude[0]
        latNum = latitude[2:]
        lonDir = longitude[0]
        lonNum = longitude[2:]
        
        coordinates = dict()
        coordinates[latDir] = int(latNum)
        coordinates[lonDir] = int(lonNum)
        
        return coordinates
    
    def requestRouteInfo(self):
        print("Enter first airport code: "),
        code1 = raw_input()
        print("Enter second airport code: "),
        code2 = raw_input() 
        print("Enter distance: "),
        try: distance = int(raw_input())
        except:
            print("Invalid distance.")
            return
        
        airport1 = self.getAirport(code1)
        airport2 = self.getAirport(code2)
        
        self.addRoute(airport1, airport2, distance)
    
    ''' Add a route, and its corresponding return route, to the database '''
    def addRoute(self, airport1, airport2, distance):    
        newFlight = Flight.flight(airport1, airport2, distance)
        newReturnFlight = Flight.flight(airport2, airport1, distance)
        
        routeCode = newFlight.getRouteCode()
        returnRouteCode = newReturnFlight.getRouteCode()
        self.flightDictionary[routeCode] = newFlight
        self.flightDictionary[returnRouteCode] = newReturnFlight
        
    def requestEditInfo(self):
        print("Enter name of the city you want to edit:"),
        cityName = raw_input()
              
        city = self.getCity(cityName)
        if (city == None):
            return
       
        print("(1) Edit City Name")
        print("(2) Edit Country")
        print("(3) Edit Continent")
        print("(4) Edit Timezone")
        print("(5) Edit Latitude/Longitude")
        print("(6) Edit Population")
        print("(7) Edit Region")
        print("(8) Edit Airport Code")
        print("Enter command: "),
        try: cmd = int(raw_input())
        except:
            print("Invalid command.")
            return
        
        self.editCommand(cmd, city)
    
    ''' Edit any of a city's 8 attributes '''
    def editCommand(self, cmd, city):
        if (cmd == 1):
            print("Enter city name: "),
            name = raw_input()
            oldName = city.getName()
            del self.cityDictionary[oldName]
            city.setName(name)
            self.cityDictionary[name] = city
        elif (cmd == 2):
            print("Enter country: "),
            country = raw_input()
            city.setCountry(country)
        elif (cmd == 3):
            print("Enter continent: "),
            continent = raw_input()
            city.setContinent(continent)
        elif (cmd == 4):
            print("Enter timezone: "),
            try: timezone = int(raw_input())
            except:
                print("Invalid timezone.")
                return
            city.setTimezone(timezone)
        elif (cmd == 5):
            print("Enter latitude (form \"DIR #\"): "),
            latitude = raw_input()
            print("Enter longitude(form \"DIR #\"): "),
            longitude = raw_input()
            coordinates = self.parseCoordinates(latitude, longitude)
            city.setCoordinates(coordinates)
        elif (cmd == 6):
            print("Enter population: "),
            try: population = int(raw_input())
            except:
                print("Invalid population.")
                return
            city.setPopulation(population)
        elif (cmd == 7):
            print("Enter region: "),
            try: region = int(raw_input())
            except:
                print("Invalid region.")
                return
            city.setRegion(region)
        elif (cmd == 8):
            print("Enter airport code: "),
            oldCode = city.getAirportCode()
            airport = self.getAirport(oldCode)
            
            newCode = raw_input()
            city.setAirportCode(newCode)
            airport.setCode(newCode)
            
            del self.airportDictionary[oldCode]
            self.airportDictionary[newCode] = airport

    ''' Writes the database back into a JSON file '''
    def writeJSON(self):
        metrosList = self.getMetrosList()
        routesList = self.getRoutesList()
        
        rawDataDictionary = {"metros" : metrosList, "routes" : routesList}
        fp = open('test.json', 'w')
        simplejson.dump(rawDataDictionary, fp, sort_keys = True, indent=5, separators = (',', ':'))
        fp.close()
    
    ''' Transfer data from city dictionary into a list '''   
    def getMetrosList(self):
        metrosList = list()
        
        cityIterator = self.cityDictionary.itervalues()
        while (True):
            try: 
                city = cityIterator.next()
            except StopIteration:
                break
            
            metroDict = {"code" : city.getAirportCode(), "name" : city.getName(), "country" : city.getCountry(), 
                         "continent" : city.getContinent(), "timezone" : city.getTimezone(), "coordinates" : city.getCoordinates(),
                         "population" : city.getPopulation(), "region" : city.getRegion()}
            
            metrosList.append(metroDict)
            
        return metrosList

    ''' Transfer data from flight dictionary into a list '''   
    def getRoutesList(self):
        routesList = list()
        
        flightIterator = self.flightDictionary.itervalues()
        while (True):
            try:
                flight = flightIterator.next()
            except StopIteration:
                break
        
            departurePort = flight.getDeparturePort()
            arrivalPort = flight.getArrivalPort()
            
            codePairList = [departurePort.getCode(), arrivalPort.getCode()]
            distance = flight.getDistance()
            flightDict = {"ports" : codePairList, "distance" : distance}
        
            routesList.append(flightDict)
        
        return routesList
    
    ''' Finds the shortest route between two cities, employing dijkstra's algorithm
        Prints out itinerary information of this route '''
    def findShortestRoute(self):
        print("Enter departure city: "),
        departureCityName = raw_input()
        print("Enter arrival city: "),
        arrivalCityName = raw_input() 
        print("")
        
        departureCity = self.getCity(departureCityName)
        arrivalCity = self.getCity(arrivalCityName)
        
        flightItinerary = self.dijkstra(departureCity, arrivalCity)
        flightItinerary.reverse()
        
        flightDistance = 0
        flightTime = float(0)
        flightCost = float(0)
        costPerKM = 0.35
        for flight in flightItinerary:
            flight.printItinerary()
            flightDistance += flight.getDistance()
            flightTime += self.calcFlightTime(flight)
            flightCost += self.calcFlightCost(flight, costPerKM)
            if (costPerKM - 0.05 > 0): costPerKM = costPerKM - 0.05
            else: costPerKM = 0
        print("Flight Distance: " + str(flightDistance) + "km")
        print("Flight Time: " + str(flightTime) + " hours")
        print("Flight Cost: " + "$" + str(flightCost))
            
    def calcFlightTime(self, flight):
        distance = flight.getDistance()
        
        if (distance > 400):
            maxVelocity = 750
            acceleratingAvgVelocity = 375
            
            acceleratingDist = 200
            uniformVelocityDist = distance - 400
            deceleratingDist = 200
            
            flightTime = (acceleratingDist + deceleratingDist) / acceleratingAvgVelocity + uniformVelocityDist / maxVelocity
        else:
            acceleration = 1406.25
            acceleratingDist = distance / 2
            uniformVelocityDist = 0
            deceleratingDist = distance / 2
            flightTime = 2 * (acceleratingDist + deceleratingDist) / math.sqrt(2 * acceleration * acceleratingDist)
            
        return flightTime
    
    def calcFlightCost(self, flight, costPerKM):
        flightCost = flight.getDistance() * costPerKM
        return flightCost
    
    ''' Dijkstra's Algorithm to find shortest path between two nodes,
        in this case, represented by airport objects '''
    def dijkstra(self, departureCity, arrivalCity):        
        departurePort = self.getPortInCity(departureCity)
        arrivalPort = self.getPortInCity(arrivalCity)
        
        if (departurePort == arrivalPort): # Do nothing
            return

        unvisitedSet = self.initializeUnvisitedSet()
                
        currentPort = departurePort        
        currentPort.shortestDistance = 0
        
        while True:
            currentPort.visited = True
            
            ### Same as "for flight in currentPort.getFlights()"
            flightIterator = currentPort.getFlights().itervalues()
            while True:
                try:
                    flight = flightIterator.next()
                except StopIteration:
                        break
            ###
                neighborPort = flight.getArrivalPort()
                if (neighborPort.visited == False): # Add only unvisited airports.
                    
                    tentativeDistance = currentPort.shortestDistance + flight.getDistance()
                    if (tentativeDistance < neighborPort.shortestDistance):
                        neighborPort.shortestDistance = tentativeDistance
                        neighborPort.previousPort = currentPort
            
                    unvisitedSet.put((neighborPort.shortestDistance, neighborPort))
            
            # Loop until you get an unvisited airport. Throw away visited airports.
            while (unvisitedSet.empty() == False and currentPort.visited == True):
                currentPort = unvisitedSet.get()[1]
            
            if (unvisitedSet.empty() == True): # Dijkstra's Algorithm complete.
                break
        
        return self.composeRouteItinerary(departurePort, arrivalPort)
    
    ''' Initializes unvisited set. Adds all airports to a priority queue with
        a shortestDistance value of infinity, no previous path information, and an
        unvisited status '''
    def initializeUnvisitedSet(self):  
        unvisitedSet = Queue.PriorityQueue()
              
        airportIterator = self.airportDictionary.itervalues()
        while True:
            try:
                airport = airportIterator.next()
            except StopIteration:
                break
            
            airport.shortestDistance = float("infinity")
            airport.previousPort = None
            airport.visited = False
            unvisitedSet.put((airport.shortestDistance, airport))
                
        return unvisitedSet
    
    ''' Records the result of Dijkstra's Algorithm by traversing from the arrival airport 
        back to the departure airport and storing connecting flights in a list '''
    def composeRouteItinerary(self, departurePort, arrivalPort):
        itinerary = []
        
        currentPort = arrivalPort
        while (currentPort != departurePort):
            previousPort = currentPort.previousPort
            currentPortCode = currentPort.getCode()
            connectingFlight = previousPort.getFlights()[currentPortCode]
            itinerary.append(connectingFlight)
            currentPort = currentPort.previousPort
            
        return itinerary
    
    def getPortInCity(self, city):
        airportCode = city.getAirportCode()
        airport = self.getAirport(airportCode)
        return airport
            
    def getRouteBetween(self, departureCode, arrivalCode):
        departurePort = self.getAirport(departureCode)
        arrivalPort = self.getAirport(arrivalCode)
        
        flights = departurePort.getFlights()
        flightIterator = flights.itervalues()
        while True:
            try: 
                flight = flightIterator.next()
            except StopIteration:
                break
            
            if (flight.getArrivalPort() == arrivalPort):
                return flight
            
        return None
        
    def close(self):
        sys.exit()