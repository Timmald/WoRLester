import gymnasium as gym
import numpy as np
import random
import math
import pygame

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
        return charArr


    def __init__(self,size):
        self.size = size
        self.stepNum = 0
        self.target_pos = np.random.randint(0,self.size-1,size=2)
        self.agent_pos = np.random.randint(0,self.size-1,size=2)
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
        self.target_pos = np.random.randint(0,self.size-1,size=2)
        self.agent_pos = np.random.randint(0,self.size-1,size=2)
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

pygame.init()
screen = pygame.display.set_mode((320, 320))
samuel = pygame.transform.scale(pygame.image.load("samuel.png").convert_alpha(), (64, 64))
goose = pygame.transform.scale(pygame.image.load("goose.png").convert_alpha(), (64, 64))
table = pygame.transform.scale(pygame.image.load("table.png").convert_alpha(), (64, 64))

mygym = DotGym(5)

clock = pygame.time.Clock()
running = True
x = 0
delta_time = 0.1

action = random.randint(0, 3)
while not mygym.step(action)[2]: # while it's not terminated
    screen.fill((255, 255, 255))
    display = mygym.display()
    for x in range(5):
        for y in range(5):
            toBlit = None
            emoji = display[x][y]
            match emoji:
                case '⬜️':
                    toBlit = goose
                case '🤮':
                    toBlit = samuel
                case '🎯':
                    toBlit = table
            screen.blit(toBlit, (64*x, 64*y))
    action = random.randint(0,3)
    pygame.display.flip()
    delta_time = clock.tick(1) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

