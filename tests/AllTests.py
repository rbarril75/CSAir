'''
Created on Sep 27, 2011

@author: Ryan
'''
import unittest
import Graph

class Test(unittest.TestCase):

    def setUp(self):
        self.graph = Graph.graph()
        
    def testGetCityCount(self):
        self.assertEqual(self.graph.getCityCount(), 48)
        
    def testFlightCount(self):
        self.assertEqual(self.graph.getFlightCount(), 188)
    
    def testGetAveragePopulation(self):
        self.assertEqual(self.graph.getAverageCityPopulation(), 11796143)
        
    def testGetAverageFlightLength(self):
        self.assertEqual(self.graph.getAverageFlightLength(), 2300)
        
    def testGetPopulation(self):
        self.assertEqual(self.graph.getCity("Mexico City").getPopulation(), 23400000)
        
    def testGetCode(self):
        self.assertEqual(self.graph.getCity('Cairo').getAirportCode(), "CAI")
           
    def testGetCountry(self):
        self.assertEqual(self.graph.getCity("Los Angeles").getCountry(), "US")
        
    def testGetName(self):
        self.assertEqual(self.graph.getCity("Sydney").getName(), "Sydney")
    
    def testGetContinent(self):
        self.assertEqual(self.graph.getCity("Toronto").getContinent(), "North America")
    
    def testGetTimezone(self):
        self.assertEqual(self.graph.getCity("Manila").getTimezone(), 8)
    
    def testGetCoordinates(self):
        self.assertEqual(self.graph.getCity("Riyadh").getCoordinates(), "(N 25, E 47)")
    
    def testGetRegion(self):
        self.assertEqual(self.graph.getCity("Johannesburg").getRegion(), 1)
        
    def testNoSuchFlight(self):
        self.assertTrue(self.graph.getRouteBetween("CHI", "NYC") == None)
        
    def testLOSTFlight815(self):
        self.assertTrue(self.graph.getRouteBetween("SYD", "LAX") != None)
    
    def testGetAirport(self):
        airport = self.graph.getAirport("SCL")
        self.assertTrue(airport.getCity().getName() == "Santiago")
        
    def testGetCity(self):
        city = self.graph.getCity("Manila")
        self.assertTrue(city.getName() == "Manila")
        
    def testGetFlight(self):
        flight = self.graph.getFlight("MIL-ESS")
        self.assertTrue(flight.getDistance() == 681)
        self.assertTrue(flight.getDeparturePort().getCity().getName() == "Milan")
        
    def testRemoveCity(self):
        city = self.graph.getCity("Essen")
        self.graph.removeCity(city)
        self.assertTrue(self.graph.cityDictionary.has_key("Essen") == False)
        
    def testAddCity(self):
        coordinates = dict()
        coordinates['N'] = 25
        coordinates['E'] = 50
        self.graph.addCity("Stamford", "US", "North America", -5, coordinates, 200000, 1, "JFK")
        self.assertTrue(self.graph.cityDictionary.has_key("Stamford"))
        
    def testAddRoute(self):
        airport1 = self.graph.getAirport("CHI")
        airport2 = self.graph.getAirport("MOW")
        distance = 10000
        self.graph.addRoute(airport1, airport2, distance)
        self.assertTrue(self.graph.getFlight("CHI-MOW") != None)
        
    def testCalcFlightTime(self):
        flight = self.graph.getFlight("MOW-THR")
        self.assertTrue(self.graph.calcFlightTime(flight) == 3.0)
        
    def testCalcFlightCost(self):
        flight = self.graph.getFlight("JNB-KRT")
        self.assertTrue(self.graph.calcFlightCost(flight, 0.35) == 1624)
        
    def testAddJSON(self):
        self.graph.populateDatabase("cmi_hub.json")
        self.assertTrue(self.graph.getCity("Champaign") != None)
             
if __name__ == "__main__":
    unittest.main()
else:
    pass