'''
Created on Sep 27, 2011

@author: Ryan
'''

''' Flight class which stores a flight's departure and arrival airports, distance, and a unique route code '''
class flight(object):

    def __init__(self, depPort, arrPort, length):
        self.departurePort = depPort
        self.arrivalPort = arrPort
        self.distance = length
        self.routeCode = self.createRouteCode(depPort, arrPort)
        
        self.departurePort.addFlight(self)
    
    ''' Creates a unique route code identifier for this flight '''
    def createRouteCode(self, depPort, arrPort):
        routeCode = depPort.getCode() + "-" + arrPort.getCode()
        return routeCode 
    
    ''' Prints out this flight's information '''
    def getItinerary(self):
        return self.departurePort.cityAndCode() + " to " + self.arrivalPort.cityAndCode() + " - " + str(self.distance) + "km"

    def printItinerary(self):
        print(self.getItinerary())
        
    def getDeparturePort(self):
        return self.departurePort
    
    def getArrivalPort(self):
        return self.arrivalPort
        
    def getDistance(self):
        return self.distance
    
    def getRouteCode(self):
        return self.routeCode               