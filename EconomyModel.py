
import random, math, numpy as np

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid, MultiGrid
from mesa.datacollection import DataCollector

# global variables
treasury = 0
incentive_pool = 0
economy_token_wealth = 0
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
            model_reporters = {"Incentive Gini index": incentive_gini},
            agent_reporters = {"Token wealth": lambda agent: agent.token_wealth}
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
        

        def grow(self): # grown agent population according to Bass diffusion model
            pass


        def run_model(self, n):
            for i in range(n):
                self.step()
                print("step = ", step())


        def step(self):
            self.datacollector.collect(self)
            # the model shuffles the order of the agents, then activates and executes each agents step method the agents
            # step method calls the methods within the AgentModel class that define agent behavior (response to incentive, ...)
            self.schedule.step()
            # self.sigmoidal_incentive_mechanism()
            # self.recursive_incentive_mechanism()




class AgentModel(Agent):

    global asset_mean
    global asset_stdev

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        global treasury, incentive_pool, economy_token_wealth

        self.asset_wealth = np.random.normal(asset_mean, asset_stdev)
        self.token_wealth = (1.0-0.3-0.05) * self.asset_wealth # @IMPLEMENT: handle decimal precision
        economy_token_wealth += self.token_wealth
        treasury += 0.3 * self.asset_wealth # 30% of the asset value is put into the treasury as protocol revenue
        incentive_pool += 0.05 * self.asset_wealth # 5% of the asset value is put into the incentive pool

    
    def choose_to_assure_asset(self):
        # start at a 50% average probability that agents will assure asset ownership and increase this as incentive is put into the economy
        # the probability is per capita average
        # a sigmoid function is 
        assurance_probability = 0.5 * incentive_pool

        assure_asset = True

        return assure_asset


    def get_incentive(self):
        if choose_to_assure_asset:
        # if the agent assures ownership of the asset during this timestep, there is a probability p (now 10%) that they will be given incentive
        # @IMPLEMENT: where p is a fraction of the number of agents who have assured ownership during this timestep
            if random.randint(1,10) == 0: # there is a 10% chance of this
                self.token_wealth += incentive_pool * (self.token_wealth / economy_token_wealth)


    def move(self):
        # might want to design some meaning into the physical position of the agent to be analogous to their position in the real world
        pass


    def transact(self):
        # perform some transaction in the economy
        pass


    k = 1 # change this to step number
    
    if k = 1:
        self.assurance_probability = 0.5

    def sigmoidal_incentive_mechanism(self):
        self.assurance_probability = 0.5 + (0.5 / 1 + math.exp(-1 * incentive_pool * (self.token_wealth / economy_token_wealth) * k)) # @IMPLEMENT step count k to mimic x along x-axis


    def recursive_incentive_mechanism(self):
        self.assurance_probability += incentive_pool * (self.token_wealth / economy_token_wealth) * (1 - self.assurance_probability)


    def step(self):
        pass



"""
        INTERNAL DOCUMENTATION

asset_means and asset_stdev:
The price of assets that an independent, unstimulated group of actors will make follow a normal distrubution. mean and stdev are the mean and
standard deviations of the price of the assets being tokenized. frac is the fraction of agents in the economy that will tokenize an asset
during the current timestep. With more incentive put into the overall economy, this fraction is expected to go up.
"""

