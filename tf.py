import numpy as np
import tensorflow as tf

data = None

# Transfer data from connection.py
def receive_data(input):
    global data
    data = input