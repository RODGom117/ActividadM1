import random
from os import remove
import numpy as np
import time
import datetime
import matplotlib.pyplot as plt
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa import Agent, Model
from mesa.batchrunner import BatchRunner
from mesa.space import MultiGrid

#Rodrigo Gomez Quiroz A01660379
"""
Room of MxN spaces.
Number of agents.
Maximum execution time.

Initialize dirty cells (random locations).
All agents start at cell [1,1].


At each time step:
If the cell is dirty, then vacuum.
the agent chooses a random direction to move.
The maximum set time is executed.
"""
#Class for the dirt
class Dirt(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.dirt = True

    def step(self):
        pass

#Class for the vacum
class Vacum(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.dirt = False
        self.x = 1
        self.y = 1
        self.model.grid.place_agent(self, (self.x, self.y))

    def step(self):
        self.dirt = False
        self.random_move()
        self.dirt = self.model.grid.is_cell_empty((self.x, self.y))

    def random_move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

#Class for the model
class VacumModel(Model):
    def __init__(self, N, width, height, max_time):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.max_time = max_time
        self.datacollector = DataCollector(
            model_reporters={"Dirt": lambda m: self.count_dirt()},
            agent_reporters={"Dirt": "dirt"}
        )

        # Create agents
        for i in range(self.num_agents):
            a = Vacum(i, self)
            self.schedule.add(a)

        # Create dirt
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            if (x != 1 or y != 1):
                if random.random() < 0.5:
                    dirt = Dirt((x, y), self)
                    self.grid.place_agent(dirt, (x, y))

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.count_dirt() == 0:
            self.running = False
        if self.schedule.steps > self.max_time:
            self.running = False

    def count_dirt(self):
        dirt = 0
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            if not self.grid.is_cell_empty((x, y)):
                dirt += 1
        return dirt

#Function to run the model
def run_model(N, width, height, max_time):
    model = VacumModel(N, width, height, max_time)
    while model.running:
        model.step()
    return model.datacollector.get_model_vars_dataframe()

#Function to run the model with batchrunner
def run_batch(N, width, height, max_time):
    fixed_params = {"N": N, "width": width, "height": height, "max_time": max_time}
    variable_params = {"N": range(1, 10)}
    batch_run = BatchRunner(VacumModel, variable_params, fixed_params, iterations=5, max_steps=100, model_reporters={"Dirt": lambda m: m.count_dirt()})
    batch_run.run_all()
    run_data = batch_run.get_model_vars_dataframe()
    return run_data

#Function to plot the data
def plot_data(data):
    plt.plot(data)
    plt.ylabel('Dirt')
    plt.xlabel('Time')
    plt.show()


