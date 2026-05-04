import time
import csv
import numpy as np
import physics
import utils

WORKERS = [1, 2, 4, 8]
CHUNKS = WORKERS, WORKERS * 2, WORKERS * 4, WORKERS * 8
STEPS = [1, 5, 10]
NUM_OF_PARTICLES = [10, 50, 100, 200, 500]
DT = 0.01


    