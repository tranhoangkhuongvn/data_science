import pandas as pd 
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt 

url = 'data/bikeshare.csv'
bikes = pd.read_csv(url)
print(bikes)

