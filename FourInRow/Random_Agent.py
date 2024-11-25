from Env import Env
from Graphics import*
import random

class Random_Agent:
    def __init__(self, player, env : Env,):
        self.player = player
        self.env = env

    def get_action_state (self, state = None):
        action = random.randint(0,6)
        while not self.env.legal(state,action):
            action = random.randint(0,6)
        return action
    
    def get_action (self, events = None, state = None):
        action = random.randint(0,6)
        if self.env.legal(self.env.state,action):
            return action
        return None
    
    def __call__(self, events):
        return self.get_action(events)