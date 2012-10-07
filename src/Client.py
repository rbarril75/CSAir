'''
Created on Sep 22, 2011

@author: Ryan
'''

import Graph
import Commands
import EventHandler

class Interface():

    def __init__(self):
        self.graph = Graph.graph()
        self.listCities = Commands.listCitiesCmd(self.graph)
        self.getCityInfo = Commands.getCityInfoCmd(self.graph)
        self.getStats = Commands.getStatsCmd(self.graph)
        self.getMap = Commands.getMapCmd(self.graph)
        self.editDatabase = Commands.editDatabaseCmd(self.graph)
        self.writeJSON = Commands.writeJSON(self.graph)
        self.shortestRoute = Commands.findShortestRoute(self.graph)
        self.addJSON = Commands.addJSON(self.graph)
        self.quit = Commands.quitCmd(self.graph)
        self.handler = EventHandler.handler(self.listCities, self.getCityInfo, self.getStats, self.getMap,
                                            self.editDatabase, self.writeJSON, self.shortestRoute, self.addJSON, self.quit)
                
    def entry(self):
        print("")
        print("ACTIONS")
        print("(1) List destination cities of CSAir")
        print("(2) Get information about a specific city")
        print("(3) Get CSAir flight statistics")
        print("(4) Get Route Map URL")
        print("(5) Edit CSAir Network")
        print("(6) Write CSAir Database to JSON File")
        print("(7) Find shortest route between two cities")
        print("(8) Add to database")
        print("(9) Quit")
        print("What would you like to do? Enter a number:"),
        
        action = raw_input()
        print("")
        
        if (action == "1"):
            self.handler.listCities()
        elif (action == "2"):
            self.handler.getCityInfo()
        elif (action == "3"):
            self.handler.getStats()
        elif (action == "4"):
            self.handler.getMap()
        elif (action == "5"):
            self.handler.editDatabase()
        elif (action == "6"):
            self.handler.writeJSON()
        elif (action == "7"):
            self.handler.findShortestRoute()
        elif (action == "8"):
            self.handler.addJSON()
        elif (action == "9"):
            self.handler.quitProgram()
        else:
            print("Invalid input.")
        
        self.entry()