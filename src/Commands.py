'''
Created on Sep 30, 2011

@author: Ryan
'''

''' Declaration and definition of command objects '''
class Command(object):

    def __init__(self):
        pass
    
    def execute(self):
        pass

class listCitiesCmd(Command):
    def __init__(self, graph):
        self.graph = graph
        
    def execute(self):
        self.graph.listCities()
        
class getCityInfoCmd(Command):
    def __init__(self, graph):
        self.graph = graph
        
    def execute(self):
        self.graph.requestCityInput()
        
class getStatsCmd(Command):
    def __init__(self, graph):
        self.graph = graph
        
    def execute(self):
        self.graph.requestStatsInput()
        
class getMapCmd(Command):
    def __init__(self, graph):
        self.graph = graph
        
    def execute(self):
        self.graph.printMapURL()
        
class editDatabaseCmd(Command):
    def __init__(self, graph):
        self.graph = graph
        
    def execute(self):
        self.graph.editGraph()
        
class writeJSON(Command): 
    def __init__(self, graph):
        self.graph = graph
        
    def execute(self):
        self.graph.writeJSON()  
        
class findShortestRoute(Command):
    def __init__(self, graph):
        self.graph = graph
        
    def execute(self):
        self.graph.findShortestRoute()  
        
class addJSON(Command):
    def __init__(self, graph):
        self.graph = graph
        
    def execute(self):
        self.graph.addJSON()  
        
class quitCmd(Command):
    def __init__(self, graph):
        self.graph = graph
        
    def execute(self):
        self.graph.close()