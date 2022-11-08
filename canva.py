from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

from vacum import  Vacum, VacumModel

def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}
    if agent.dirt:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.2
    else:
        portrayal["Color"] = "black"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.5
    return portrayal

grid = CanvasGrid(agent_portrayal, 5, 5, 500, 500)
chart = ChartModule([{"Label": "Dirt", "Color": "Black"}])

server = ModularServer(VacumModel,
                          [grid, chart],        
                            "Vacum Model",
                            {"N": 5, "width": 5, "height": 5, "max_time": 20})
server.port = 8521 # The default
server.launch()