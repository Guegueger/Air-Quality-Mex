import pickle
import os

path = r'C:\Users\hgera\OneDrive\Escritorio\GITHUB\Air-Quality-Mex\data\data_PowerBI.pkl'
path = path.replace('\\', os.sep)

with open(path, 'rb') as f:
    data= pickle.load(f)

print(data)