from gym import DotGym
import numpy as np
import random
import matplotlib.pyplot as plt

mygym = DotGym()
table = np.ndarray(shape=(30,31,4),dtype=float)
tableCounts = np.zeros((30,31,4))
table.fill(-9999)
randChance = .2
numtrials = 80
stepNums = []
for i in range(numtrials):
    print(f"TRIAL {i}: ",)
    pos = mygym.reset()["agent"]
    done = False
    done2 = False
    actions = []
    totalReward = 0
    while not (done or done2):
        action = np.argmax(table[pos[0]][pos[1]]/(tableCounts[pos[0]][pos[1]]+1))#find highest reward action from cur pos
        if np.random.choice([True,False],p=[randChance,1-randChance]):
            action = random.randint(0,3)#Least done action?
        actions.append((pos[0],pos[1],action))
        state, reward, done,done2 = mygym.step(action,headless=True)
        pos = state["agent"]
        totalReward += reward
    print(f"Reward: {totalReward}, NumSteps: {len(actions)}")
    #update the table
    for x,y,action in actions:
        tableCounts[x][y][action]+=1
        table[x][y][action] += totalReward
    stepNums.append(len(actions))
plt.plot(stepNums)
plt.show()