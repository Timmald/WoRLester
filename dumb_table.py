from gym import DotGym
import numpy as np
import random
import matplotlib.pyplot as plt
import pygame
import math
import pickle

pygame.init()
mygym = DotGym()
table = np.ndarray(shape=(30,31,4),dtype=float)
tableCounts = np.zeros((30,31,4))
table.fill(0)
 #TODO: Change this over time?
i = 0
stepNums = []
totalRewards = []
while True:
    randChance = .3
    print(f"TRIAL {i}: ",)
    pos = mygym.reset()["agent"]
    done = False
    done2 = False
    actions = []
    totalReward = 0
    while not (done or done2):
        action = np.argmax(table[pos[0]][pos[1]]/(tableCounts[pos[0]][pos[1]]+1))#find highest reward action from cur pos
        if np.random.choice([True,False],p=[randChance,1-randChance]):
            action = random.randint(0,3)#TODO:Least done action?
        actions.append((pos[0],pos[1],action))
        state, reward, done,done2 = mygym.step(action,headless=True)
        pos = state["agent"]
        totalReward = (1-.3)*totalReward+.3*reward
    totalRewards.append(totalReward)
    print(f"Reward: {totalReward}, NumSteps: {len(actions)}")
    #update the table
    for x,y,action in actions:
        tableCounts[x][y][action]+=1
        table[x][y][action] += totalReward
    randChance = 1/(.25*(math.sqrt(i+1)))
    stepNums.append(len(actions))
    if i%50 == 0:
        avg = np.average(totalRewards)
        totalRewards = []
        with open(f"models/{i}_{avg}.pickle","wb") as pick:
            pickle.dump((table,tableCounts),pick)
    i+=1

#TODO: It's learning to press against a table
#for i in range(5):
    #pos = mygym.reset()["agent"]
    #done = False
    #done2 = False
    #while not (done or done2):
        #action = np.argmax(table[pos[0]][pos[1]]/(tableCounts[pos[0]][pos[1]]+1))#find highest reward action from cur pos
        #state, reward, done,done2 = mygym.step(action=action)
        #pos = state["agent"]
plt.plot([float(np.average(stepNums[i:i+2])) for i in range(len(stepNums)-2)])
plt.show()