import gymnasium as gym
import numpy as np
import random
import math

class DotGym(gym.Env):

    def distance(self,coord1,coord2):
        return math.sqrt((coord2[0]-coord1[0])**2+(coord2[1]-coord1[1])**2)

    def display(self):
        charArr = []
        for i in range(self.size):
            charArr.append(["⬜️"]*self.size)#TODO: Pointer shit
        charArr[self.agent_pos[0]][self.agent_pos[1]] = "🤮"
        charArr[self.target_pos[0]][self.target_pos[1]] = "🎯"
        print("-------------------")
        print(f"STEP #{self.stepNum}:")
        for line in charArr:
            for char in line:
                print(char,end="")
            print("\n")


    def __init__(self,size):
        self.size = size
        self.stepNum = 0
        self.target_pos = np.random.random_integers(0,self.size-1,size=2)
        self.agent_pos = np.random.random_integers(0,self.size-1,size=2)
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
        self.target_pos = np.random.random_integers(0,self.size-1,size=2)
        self.agent_pos = np.random.random_integers(0,self.size-1,size=2)
        self.stepNum = 0
        return {"agent":self.agent_pos,"target":self.target_pos}
    
    def step(self,action):
        self.agent_pos = list(np.clip(np.array(self.agent_pos)+np.array(self.action_to_direction[action]),0,self.size-1))
        reward = -1*self.distance(self.target_pos,self.agent_pos)
        truncated = False
        terminated = all(self.agent_pos == self.target_pos)
        self.stepNum+=1
        self.display()
        return {"agent":self.agent_pos,"target":self.target_pos},reward,terminated,truncated

mygym = DotGym(5)
action = random.randint(0,3)
while not mygym.step(action)[2]: #while it's not terminated
    action = random.randint(0,3)

        