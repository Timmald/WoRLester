import gymnasium as gym
import numpy as np
import random
import math
import pygame
import time

class Table:
    def __init__(self, coords):
        self.coords = coords
        self.open = random.choice([True,False])
    def update(self):
        self.open = random.choice([True,False])
class DotGym(gym.Env):

    def get_obs(self):
        return {"agent":self.agent_pos} #TODO: Change the state

    def distance(self,coord1,coord2):
        return math.sqrt((coord2[0]-coord1[0])**2+(coord2[1]-coord1[1])**2)

    def inObs(self,coords:list[int,int],tabs=True):
        if tabs:
            fullTabs = [tab for tab in self.tables if not tab.open]
            for obs in self.obstacles:
                if obs[0][0]<=coords[0]<=obs[1][0] and obs[0][1]<=coords[1]<=obs[1][1]:
                    return True
            if any([all(tab.coords == coords) for tab in fullTabs]):
                return True
            return False
        else:
            for obs in self.obstacles:
                if obs[0][0]<=coords[0]<=obs[1][0] and obs[0][1]<=coords[1]<=obs[1][1]:
                    return True
            return False

    def hasWon(self):
        return any([all(self.agent_pos == tab.coords) for tab in self.tables if tab.open])

    def genTableCoords(self):
        tableCoords = np.random.random_integers(0,self.size-1,size=2)
        while self.inObs(tableCoords,tabs = False):
            tableCoords = np.random.random_integers(0,self.size-1,size=2)
        return tableCoords

    def updateTables(self):
        for tab in self.tables:
            tab.update()

    def display(self):
        self.screen.fill((255, 255, 255))
        for x in range(self.size):
            for y in range(self.size):
                toBlit = None
                doubleBlit = False
                if self.agent_pos == [x, y]:
                    toBlit = self.samuel
                for tab in self.tables:
                    if all(tab.coords == [x, y]):
                        toBlit = self.table
                        if not tab.open:
                            doubleBlit = True
                for obs in self.obstacles:
                    if x in range(obs[0][0], obs[1][0]+1):
                        if y in range(obs[0][1], obs[1][1]+1):
                            toBlit = self.javier
                if not toBlit:
                    continue
                self.screen.blit(toBlit, (64*x, 64*y))
                if doubleBlit:
                    self.screen.blit(self.goose, (64*x, 64*y))
        pygame.display.flip()
        time.sleep(.1)
        # actionList = ["➡️","⬇️","⬅️","⬆️"]
        # charArr = []
        # for i in range(self.size):
        #     charArr.append(["⬜️"]*self.size)
        # charArr[self.agent_pos[0]][self.agent_pos[1]] = "🤮"
        # for tab in self.tables:
        #     charArr[tab.coords[0]][tab.coords[1]] = "🍴" if tab.open else "🚫"
        # for obs in self.obstacles:
        #     for row in range(obs[0][0],obs[1][0]+1):
        #         for col in range(obs[0][1],obs[1][1]+1):
        #             charArr[row][col] = "🆘"
        # print("-------------------")
        # print(f"STEP #{self.stepNum}: {actionList[self.last_action]}")
        # for line in charArr:
        #     for char in line:
        #         print(char,end="")
        #     print("\n")


    def __init__(self):
        self.screen = pygame.display.set_mode((64 * 10, 64 * 10))
        self.samuel = pygame.transform.scale(pygame.image.load("samuel.png").convert_alpha(), (64, 64))
        self.goose = pygame.transform.scale(pygame.image.load("goose.png").convert_alpha(), (64, 64))
        self.table = pygame.transform.scale(pygame.image.load("table.png").convert_alpha(), (64, 64))
        self.javier = pygame.transform.scale(pygame.image.load("javier.png").convert_alpha(), (64, 64))
        self.clock = pygame.time.Clock()
        self.delta_time = 0.1
        self.update_interval = 5
        self.size = 10
        self.stepNum = 0
        self.obstacles = [((3,2),(5,6))]
        self.tables = [Table(self.genTableCoords())for i in range(4)]
        self.agent_pos = np.random.random_integers(0,self.size-1,size=2)
        self.obs_space = gym.spaces.Dict({
            "agent":gym.spaces.Box(0,self.size-1,shape=(2,),dtype=int),
            "target":gym.spaces.Box(0,self.size-1,shape=(2,),dtype=int)#TODO: Change the state
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
        self.agent_pos = np.random.random_integers(0,self.size-1,size=2)
        self.stepNum = 0
        return self.get_obs()
    
    def reward(self):
        isOpenTable = any([tab.open for tab in self.tables])
        if isOpenTable:
            return -1*self.distance(sorted([tab for tab in self.tables if tab.open],key=lambda x:self.distance(x.coords,self.agent_pos))[0].coords,self.agent_pos)
        else:
            return -9999

    def step(self,action):
        if self.stepNum % self.update_interval == 0:
            self.updateTables()
        self.last_action = action
        newCoord = list(np.clip(np.array(self.agent_pos)+np.array(self.action_to_direction[action]),0,self.size-1))
        self.agent_pos = newCoord if not self.inObs(newCoord) else self.agent_pos
        reward = self.reward()
        truncated = False
        terminated = self.hasWon()
        self.stepNum+=1
        self.display()
        return self.get_obs(),reward,terminated,truncated


mygym = DotGym()
pygame.init()

action = random.randint(0, 3)
while not mygym.step(action)[2]: # while it's not terminated
    action = random.randint(0, 3)
