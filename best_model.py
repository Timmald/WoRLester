from gym import DotGym
import os
import pickle
import numpy as np
import random

best = sorted(os.listdir("models"),key=lambda x: float(x[:-7].split("_")[1]))[-1]
print(best)
with open(f"models/{best}","rb") as pickler:
    table,tableCounts = pickle.load(pickler)
mygym = DotGym()
pos = mygym.reset()["agent"]
done = False
trunc = False
while not (done or trunc):
    action = np.random.choice([np.argmax(table[pos[0]][pos[1]]/(tableCounts[pos[0]][pos[1]]+1)),random.randint(0,3)],p=[.8,.2])
    state,reward,done,trunc = mygym.step(action)
    pos = state["agent"]