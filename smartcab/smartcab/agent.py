import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import numpy as np

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env, learning_rate=0.71, discount_factor=0.36):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.Q = {}
        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.actions = Environment.valid_actions
        self.oldAction = None


    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.oldAction=None
    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        #------------------------------------------------
        #action = np.random.choice(self.actions)
        #------------------------------------------------
        


        # TODO: Select action according to your policy
        current_state = tuple(inputs.values() + [self.next_waypoint])
        self.state = (inputs, self.next_waypoint)
        
        if current_state not in self.Q:
        	self.Q[current_state] = [3,3,3,3]

        Q_max = self.Q[current_state].index(np.max(self.Q[current_state]))
        # Execute action and get reward
        action = self.actions[Q_max]
        reward = self.env.act(self, action)



        # TODO: Learn policy based on state, action, reward
        
        if t!=0:
			oldvalue = self.Q[self.oldAction[0]][self.oldAction[1]]
			newvalue = ((1 - self.learning_rate)*oldvalue)+(self.learning_rate * (self.oldAction[2] + self.discount_factor * self.Q[current_state][Q_max]))
			self.Q[self.oldAction[0]][self.oldAction[1]] = newvalue 
        
        self.oldAction = (current_state, self.actions.index(action), reward)
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]
   
       

def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=False)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=1.0)  # reduce update_delay to speed up simulation
    sim.run(n_trials=10)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    run()
