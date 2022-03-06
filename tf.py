import numpy as np
import tensorflow as tf

data = None

def receive_data(input):
    global data
    data = input