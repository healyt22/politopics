import os
import numpy as np
from sklearn import metrics
import seaborn as sb
import matplotlib.pyplot as plt

from preprocess import *

class DiffusionMap():
    def __init__(self, handle):
        self.obj = Preprocess(handle)
