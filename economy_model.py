
import random, math, numpy as np

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

# global variables
treasury = 0
asset_mean = 500
asset_stdev = 100

def incentive_gini():
    # this method computes the degree of disparity in the reaction to incentives among agents in the economy
    pass


class EconomyModel(Model):

    def __init__(self, num_agents, height, width):
        self.num_agents = num_agents
        self.running = True
        self.grid = SingleGrid(height, width, True)
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
            self.grid.place_agent(agent, (x,y))
        

        def step(self):
            self.datacollector.collect(self)
            self.schedule.step()



class AgentModel(Agent):

    global asset_mean
    global asset_stdev
    global treasury

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        self.asset_wealth = np.random.normal(asset_mean, asset_stdev)
        self.token_wealth = 0.7 * self.asset_wealth
        treasury += 0.3 * self.asset_wealth


    def move(self):
        # might want to design some meaning into the physical position of the agent to be analogous to their position in the real world
        pass


    def transact(self):
        # perform some transaction in the economy
        pass


    def step(self):
        pass


baseModel = EconomyModel(100, 10, 10)


"""
        INTERNAL DOCUMENTATION

asset_means and asset_stdev:
The price of assets that an independent, unstimulated group of actors will make follow a normal distrubution. mean and stdev are the mean and
standard deviations of the price of the assets being tokenized. frac is the fraction of agents in the economy that will tokenize an asset
during the current timestep. With more incentive put into the overall economy, this fraction is expected to go up.
"""

