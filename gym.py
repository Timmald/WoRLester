import gymnasium as gym
import numpy as np
import random
import math

class DotGym(gym.Env):

    def distance(self,coord1,coord2):
        return math.sqrt((coord2[0]-coord1[0])**2+(coord2[1]-coord1[1])**2)

    def display(self):
        charArr = ["⬜️"]*self.size*self.size
        charArr[self.agent_pos[0]][self.agent_pos[1]] = "🕵️"
        charArr[self.target_pos[0]][self.target_pos[1]] = "🎯"
        print("-------------------")
        for line in charArr:
            print(line)


    def __init__(self,size):
        self.size = size
        self.target_pos = [-1,-1]
        self.agent_pos = [-1,-1]
        self.obs_space = gym.spaces.Dict({
            "agent":gym.spaces.Box(0,size-1,shape=(2,),dtype=int),
            "target":gym.spaces.Box(0,size-1,shape=(2,),dtype=int)
        })
        self.action_space = gym.spaces.Discrete(4)
        self.action_to_direction = {
            0:[0,1],
            1:[1,0],
            2:[0,-1],
            3:[-1,0]
        }

    def reset(self,seed):
        super().reset(seed)
        self.target_pos = np.random_integers(0,self.size-1,size=2,dtype=int)
        self.agent_pos = np.random_integers(0,self.size-1,size=2,dtype=int)
        return {"agent":self.agent_pos,"target":self.target_pos}
    
    def step(self,action):
        self.agent_pos = list(np.array(self.agent_pos)+np.array(self.action_to_direction[action]))
        reward = -1*self.distance(self.target_pos,self.agent_pos)
        truncated = False
        terminated = self.agent_pos == self.target_pos
        self.display()
        return {"agent":self.agent_pos,"target":self.target_pos},reward,terminated,truncated

mygym = DotGym(5)
mygym.step()
        