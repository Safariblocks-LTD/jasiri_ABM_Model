import random, math, numpy as np

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid, MultiGrid
from mesa.datacollection import DataCollector

# global variables
treasury = 0
incentive_pool = 0
economy_token_wealth = 1
asset_mean = 500    # for when agents are first tokenizing assets
asset_stdev = 100

def incentive_gini():
    # this method computes the degree of disparity in the reaction to incentives among agents in the economy
    # proportional to the variance in agents' probability of assuring an asset
    pass


class EconomyModel(Model):

    def __init__(self, num_agents, height, width):
        self.num_agents = num_agents
        self.running = True
        self.grid = MultiGrid(height, width, True)
        self.schedule = RandomActivation(self)
        self.model_assurace_probability = 0
        self.datacollector = DataCollector(
        )

        # create agents
        for agent_index in range(self.num_agents):
            agent = AgentModel(agent_index, self)
            self.schedule.add(agent)
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            try:
                self.grid.place_agent(agent, (x, y))
            except Exception:
                self.grid.place_agent(agent, self.grid.find_empty) # could just use this to place agents then
    

    def update_model_assurace_probability(self):
        sum = 0
        for agent in self.schedule.agents:
            sum += agent.assurance_probability
        self.model_assurace_probability = sum / self.num_agents

        # grown agent population according to Bass diffusion model, incorporate decrease
    def grow(self):
        pass

        #
    def execute_model(self, n):
        for i in range(n):
            self.step()
            print("step = ", self.step())

    def step(self):
        self.datacollector.collect(self)
            # the model shuffles the order of the agents, then activates and executes each agents step method the agents
            # step method calls the methods within the AgentModel class that define agent behavior (response to incentive, ...)
            #print(f"This is run number {run_i}.")
        self.schedule.step()
        self.update_model_assurace_probability()
        print(f"Model assurance probability is {self.model_assurace_probability}.")





class AgentModel(Agent):

    global asset_mean
    global asset_stdev

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        global treasury, incentive_pool, economy_token_wealth

        self.asset_wealth = np.random.normal(asset_mean, asset_stdev)
        self.token_wealth = (1.0-0.3-0.05) * self.asset_wealth # @IMPLEMENT: handle decimal precision
        self.has_transacted = False
        self.incentive = incentive_pool * (self.token_wealth / economy_token_wealth)
        self.assurance_probability = np.random.normal(0.7, 0.1)
        while (self.assurance_probability < 0 or self.assurance_probability > 1):
            self.assurance_probability = np.random.normal(0.7, 0.1)

        economy_token_wealth += self.token_wealth
        treasury += 0.3 * self.asset_wealth # 30% of the asset value is put into the treasury as protocol revenue
        incentive_pool += 0.05 * self.asset_wealth # 5% of the asset value is put into the incentive pool

    # Now when there is a step/ iteration in the model, this will be applied to agents who assure their wealth
    # of the agents who have assured their wealth, 1/frac is the fraction that is to be rewarded randomly
    def get_incentive(self, frac):
        if random.randint(1,frac) == 1: # there is a 1/frac chance of this
            self.token_wealth += self.incentive
            self.sigmoidal_incentive_mechanism(self.incentive)

    def move(self):
        # might want to design some meaning into the physical position of the agent to be analogous to their po sition in the real world
        pass

    # randomly transact with pool
    def transact(self):
        # perform some transaction in the economy
        self.has_transacted = True

    # the incentive pool can decrease if more is given out than is put in
    def sigmoidal_incentive_mechanism(self, incentive):
        self.assurance_probability = 0.1 + (0.9 / 1 + math.exp(-1 * incentive)) # @IMPLEMENT step count k to mimic x along x-axis

    def recursive_incentive_mechanism(self, incentive):
        self.assurance_probability += incentive * (1 - self.assurance_probability)

    # as a fraction of agents who assure ownership are rewarded randomly, those who are not are slightly less likely to assure ownership next
    def non_incentivization_effect(self):
        if self.has_transacted:
            self.assurance_probability *= 0.95
        else:
            self.assurance_probability *= 0.85

    def step(self):
        # self.sigmoidal_incentive_mechanism(self.incentive)
        print(f"My assurance probability is {self.assurance_probability}")
        print()



if __name__ == "__main__":

    economyModel = EconomyModel(3, 10, 10)

    #for run_i in range(2):
    #    economyModel.step()
    economyModel.execute_model(1)




"""
        INTERNAL DOCUMENTATION

asset_means and asset_stdev:tokenized. frac is the fraction of agents in the economy that will tokenize an asset
during the current timestep. With more incentive put into the overall economy, this fraction is expected to go up.

We will let the average probability of assuring an asset in the network start at 0.55 and as it goes up with incentive put into
the economy, let this fraction of agents assuring ownership

@IMPLEMENT
decay of p_k=0 = 0 under no incentivization

"""