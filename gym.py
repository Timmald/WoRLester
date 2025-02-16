import gymnasium as gym
import numpy as np
import random
import math
import pygame
import time

class DotGym(gym.Env):

    def get_obs(self):
        return {"agent":self.agent_pos} #TODO: Change the state

    def distance(self,coord1,coord2):
        return math.sqrt((coord2[0]-coord1[0])**2+(coord2[1]-coord1[1])**2)

    def isTable(self,coord):
        return self.map[coord[0]][coord[1]]== "🚫" or self.map[coord[0]][coord[1]]== "🍴"

    def hasWon(self):
        return self.isTable(self.agent_pos)

    def getTablePos(self):
        lis = []
        for row in range(len(self.map)):
            for char in range(len(self.map[row])):
                if self.isTable([row,char]):
                    lis.append([row,char])
        return lis


    def updateTables(self):
        for row in range(len(self.map)):
            for char in range(len(self.map[row])):
                if self.isTable([row,char]):
                    self.map[row][char] = ["🚫","🍴"][np.random.choice([0,1],p=[.9,.1])]

    def display(self):
        self.screen.fill((255, 255, 255))
        for x in range(len(self.map)):
            for y in range(len(self.map[0])):
                toBlit = None
                doubleBlit = False
                curChar = self.map[y][x]
                if list(self.agent_pos) == [y,x]:
                    toBlit = self.samuel
                elif curChar == "🆘":
                    toBlit = self.javier
                elif self.isTable([y,x]):
                    if curChar == "🚫":
                        doubleBlit = True
                    toBlit = self.table
                if not toBlit:
                    continue
                self.screen.blit(toBlit, (self.square_size*x,self.square_size*y))
                if doubleBlit:
                    self.screen.blit(self.goose, (self.square_size*x,self.square_size*y))
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
        self.square_size = 28
        self.screen = pygame.display.set_mode((self.square_size * 31, self.square_size * 31))
        self.samuel = pygame.transform.scale(pygame.image.load("samuel.png").convert_alpha(), (self.square_size, self.square_size))
        self.goose = pygame.transform.scale(pygame.image.load("goose.png").convert_alpha(), (self.square_size, self.square_size))
        self.table = pygame.transform.scale(pygame.image.load("table.png").convert_alpha(), (self.square_size, self.square_size))
        self.javier = pygame.transform.scale(pygame.image.load("javier.png").convert_alpha(), (self.square_size, self.square_size))
        self.clock = pygame.time.Clock()
        self.delta_time = 0.1
        with open("map.txt","r") as reader:
            self.map = [list(l.strip()) for l in reader.readlines()]
        self.update_interval = 5
        self.stepNum = 0
        self.agent_pos = np.random.random_integers(0,min(len(self.map),len(self.map[0])),size=2)
        while not self.validCoord(self.agent_pos):
            self.agent_pos = np.random.random_integers(0,min(len(self.map),len(self.map[0])),size=2)
        self.obs_space = gym.spaces.Dict({#TODO: Fix state
            "agent":gym.spaces.Box(0,min(len(self.map),len(self.map[0])),shape=(2,),dtype=int),
            "target":gym.spaces.Box(0,min(len(self.map),len(self.map[0])),shape=(2,),dtype=int)#TODO: Change the state
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
        self.agent_pos = np.random.random_integers(0,min(len(self.map),len(self.map[0])),size=2)
        self.stepNum = 0
        return self.get_obs()
    

    def validCoord(self, coord):
        char = self.map[coord[0]][coord[1]]
        return char == "_" or char =="🍴"

    def reward(self):
        try:
            return -1*self.distance(sorted([tab for tab in self.getTablePos() if self.map[tab[0]][tab[1]]=="🍴"],key=lambda x:self.distance(x,self.agent_pos))[0],self.agent_pos)
        except:
            return -9999

    def step(self,action):
        if self.stepNum % self.update_interval == 0:
            self.updateTables()
        self.last_action = action
        
        newCoord = list(np.array([np.clip(self.agent_pos[0]+self.action_to_direction[action][0], 0, len(self.map)-1),  # Limit x within [x_min, x_max]
        np.clip(self.agent_pos[1]+self.action_to_direction[action][1], 0, len(self.map[0])-1)   # Limit y within [y_min, y_max]
        ]))

        self.agent_pos = newCoord if self.validCoord(newCoord) else self.agent_pos
        reward = self.reward()
        truncated = False
        terminated = self.hasWon()
        self.stepNum+=1
        self.display()
        return self.get_obs(),reward,terminated,truncated

if __name__ == "__main__":
    mygym = DotGym()
    pygame.init()

    action = random.randint(0, 3)
    while not mygym.step(action)[2]: # while it's not terminated
        action = random.randint(0, 3)
