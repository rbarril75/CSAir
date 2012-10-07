'''
Created on Sep 27, 2011

@author: Ryan
'''

''' City class which store's a city's attributes '''
class city(object):

    def __init__(self, name, country, continent, timezone, coordinates, population, region, code):
        self.name = name
        self.country = country
        self.continent = continent
        self.timezone = timezone
        self.coordinates = self.extractStringValue(coordinates)
        self.population = population
        self.region = region
        self.airportCode = code
    
    ''' Extracts latitude/longitude information from a dictionary and returns it in string form '''
    def extractStringValue(self, coordinates):
        
        coordinates = coordinates.iteritems()
        
        longitude = coordinates.next()
        longitudeDirection = str(longitude[0])
        longitudeValue = str(longitude[1])
                        
        latitude = coordinates.next()
        latitudeDirection = str(latitude[0])
        latitudeValue = str(latitude[1])  
              
        coordinatesString = "(" + latitudeDirection + " " + latitudeValue 
        coordinatesString += ", " + longitudeDirection + " " + longitudeValue + ")"
        
        return coordinatesString
    
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name
    
    def getCountry(self):
        return self.country
    
    def setCountry(self, country):
        self.country = country
    
    def getContinent(self):
        return self.continent
    
    def setContinent(self, continent):
        self.continent = continent
    
    def getTimezone(self):
        return self.timezone
    
    def setTimezone(self, timezone):
        self.timezone = timezone
    
    def getCoordinates(self):
        return self.coordinates
    
    def setCoordinates(self, coordinates):
        self.coordinates = coordinates
    
    def getPopulation(self):
        return self.population
    
    def setPopulation(self, population):
        self.population = population
    
    def getRegion(self):
        return self.region
    
    def setRegion(self, region):
        self.region = region
    
    def getAirportCode(self):
        return self.airportCode

    def setAirportCode(self, airportCode):
        self.airportCode = airportCode