import os
import random
import matplotlib.pyplot as plt
from obspy import read


def run(folder, count):
    count = int(count)
    for i, filename in enumerate(random.sample(os.listdir(folder), k=count)):
        filepath = os.path.join(folder, filename)
        trace = read(filepath)[0]
        trace.plot()
