'''
Created on Sep 26, 2011

@author: Ryan
'''

""" The INVOKER class"""

class handler(object):

    def __init__(self, listCitiesCmd, getCityInfoCmd, getStatsCmd, getMapCmd, 
                 editDatabaseCmd, writeJSONCmd, shortestRouteCmd, addJSONCmd, quitCmd):
        self.listCitiesCommand = listCitiesCmd
        self.getCityInfoCommand = getCityInfoCmd
        self.getStatsCommand = getStatsCmd
        self.getMapCommand = getMapCmd
        self.editDatabaseCommand = editDatabaseCmd
        self.writeJSONCommand = writeJSONCmd
        self.shortestRouteCommand = shortestRouteCmd
        self.addJSONCommand = addJSONCmd
        self.quitCommand = quitCmd
        
    def listCities(self):
        self.listCitiesCommand.execute()
    def getCityInfo(self):
        self.getCityInfoCommand.execute()
    def getStats(self):
        self.getStatsCommand.execute()
    def getMap(self):
        self.getMapCommand.execute()
    def editDatabase(self):
        self.editDatabaseCommand.execute()
    def writeJSON(self):
        self.writeJSONCommand.execute()
    def findShortestRoute(self):
        self.shortestRouteCommand.execute()
    def addJSON(self):
        self.addJSONCommand.execute()
    def quitProgram(self):
        self.quitCommand.execute()
