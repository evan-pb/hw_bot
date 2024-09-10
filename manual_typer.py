import random as r
import pyautogui as pag
import numpy as np
import time as t
import fullbot as F

with open("string.txt") as f:
    string = f.read()
t.sleep(5)
times = np.linspace(0.01, 0.07, 4)
for word in string.split(" "):
    F.typo(word, True) if r.random() < 0.025 else None
    pag.write(word, interval=r.choice(times))
    F.typo(word, False) if r.random() < 0.025 else None
    pag.write(" ")