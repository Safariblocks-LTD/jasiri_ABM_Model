
import random, math, numpy as np

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid, MultiGrid
from mesa.datacollection import DataCollector

# global variables
treasury = 0
incentive_pool = 0
asset_mean = 500
asset_stdev = 100

def incentive_gini():
    # this method computes the degree of disparity in the reaction to incentives among agents in the economy
    pass


class EconomyModel(Model):

    def __init__(self, num_agents, height, width):
        self.num_agents = num_agents
        self.running = True
        self.grid = MultiGrid(height, width, True)
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            model_reporters = {},
            agent_reporters = {}
        )

        # create agents
        for agent_index in range(self.num_agents):
            agent = AgentModel(agent_index, self)
            self.schedule.add(agent)
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            try:
                self.grid.place_agent(agent, (x,y))
            except:
                self.grid.place_agent(agent, self.grid.find_empty)
        

        def step(self):
            self.datacollector.collect(self)
            self.schedule.step()


        def grow(self): # grown agent population according to Bass diffusion model
            pass



class AgentModel(Agent):

    global asset_mean
    global asset_stdev

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        global treasury, incentive_pool

        self.asset_wealth = np.random.normal(asset_mean, asset_stdev)
        self.token_wealth = 0.7 * self.asset_wealth
        treasury += 0.3 * self.asset_wealth
        incentive_pool += 0.05 * incentive_pool



    def move(self):
        # might want to design some meaning into the physical position of the agent to be analogous to their position in the real world
        pass


    def transact(self):
        # perform some transaction in the economy
        pass


    def step(self):
        pass



"""
        INTERNAL DOCUMENTATION

asset_means and asset_stdev:
The price of assets that an independent, unstimulated group of actors will make follow a normal distrubution. mean and stdev are the mean and
standard deviations of the price of the assets being tokenized. frac is the fraction of agents in the economy that will tokenize an asset
during the current timestep. With more incentive put into the overall economy, this fraction is expected to go up.
"""

