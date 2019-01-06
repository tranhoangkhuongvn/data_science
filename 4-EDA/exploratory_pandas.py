import pandas as pd
from matplotlib import pyplot as plt

users = pd.read_table('./data/user.tbl', sep='|')
print(type(users))
