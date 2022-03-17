import tensorflow as tf
import numpy as np

data = None

# Transfer data from connection.py
def receive_data(input):
    global data
    data = input