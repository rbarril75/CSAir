'''
Created on Sep 30, 2011

@author: Ryan
'''

''' Airport class which stores an airport's code, city, and outgoing flights '''
class airport(object):

    def __init__(self, code, city, flights):
        self.code = code
        self.city = city
        self.flights = flights # Dictionary that maps destination airport codes to flight objects.
        
        # Dijikstra's Variables
        self.shortestDistance = -1
        self.previousPort = None
        self.visited = False
        
    def getCode(self):
        return self.code
    
    def setCode(self, code):
        self.code = code
    
    def getCity(self):
        return self.city
    
    def getFlights(self):
        return self.flights
    
    ''' Returns flights in a list rather than a dictionary '''
    def getListOfFlights(self):
        listOfFlights = []
        flightIterator = self.flights.itervalues()
        while True:
            try:
                flight = flightIterator.next()
            except StopIteration:
                break
            
            listOfFlights.append(flight)
            
        return listOfFlights
    
    ''' Adds a new flight to this airport, making sure to avoid duplicates '''
    def addFlight(self, flight):
        arrivalPort = flight.getArrivalPort()
        arrivalRouteCode = arrivalPort.getCode()
        
        if arrivalRouteCode not in self.flights:
            self.flights[arrivalRouteCode] = flight
        else:
            print("Duplicate flight error.")
        
    def removeFlight(self, flight):
        arrivalPort = flight.getArrivalPort()
        arrivalRouteCode = arrivalPort.getCode()
        
        if arrivalRouteCode not in self.flights:
            print"No such flight in the database."
        else:
            del self.flights[arrivalRouteCode]
        
    def printFlights(self):
        flightInfo = ""
        
        flightIterator = self.flights.itervalues()
        while True:
            try:
                flight = flightIterator.next()
            except StopIteration:
                break
        
            arrivalPort = flight.getArrivalPort()
            flightDistance = flight.getDistance()
            flightInfo += arrivalPort.cityAndCode() + " - " + str(flightDistance) + "km; "
            
        print("Outgoing Flights: " + flightInfo)
        
    def cityAndCode(self):
        ccString = self.city.getName() + " (" + self.code + ")"
        return ccString