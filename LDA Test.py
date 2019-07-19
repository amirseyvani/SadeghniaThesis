import pandas as pd
import hazm

data = pd.read_csv('Data/abcnews-date-text.csv')
data_text = data['headline_text']
data_text['index'] = data_text.index
documents = data_text
print(documents

