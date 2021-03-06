# -*- coding: utf-8 -*-
"""Preprocessing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1d4r3AnXTL4oUQieXFR3lNMy5pSgFBSF_
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import numpy as np

#preprocess
#reference: https://github.com/VasiliyRubtsov/wsdm_music_recommendations/blob/master/pipeline.ipynb
date_columns = ['expiration_date', 'registration_init_time']

train_data = pd.read_csv('music_data_raw/train.csv')
test_data = pd.read_csv('music_data_raw/test.csv', index_col=0)
item_data = pd.read_csv('music_data_raw/songs.csv')
user_data = pd.read_csv('music_data_raw/members.csv', parse_dates=date_columns)

all_data = pd.concat([train_data, test_data], sort=True)

all_data = all_data.merge(item_data, on='song_id', how='left')
all_data = all_data.merge(user_data, on='msno', how='left')

all_data.head()

all_data.isnull().any()

enc = LabelEncoder()

for col in [
    'msno', 'song_id', 'source_screen_name', 
    'source_system_tab', 'source_type', 'genre_ids', 
    'artist_name', 'composer', 'lyricist', 'gender'
]:
    all_data[col] = enc.fit_transform(all_data[col].fillna('nan'))
    
for col in ['language', 'city', 'registered_via']:
    all_data[col] = enc.fit_transform(all_data[col].fillna(-2))
    

# Question: Why is this time column needed
all_data['time'] = all_data.index / len(all_data)

n = len(train_data)
#train_data = all_data[:n]
#test_data = all_data[n:]

# train_data.to_hdf('music_data_raw/train_data.hdf', key='wsdm')
# test_data.to_hdf('music_data_raw/test_data.hdf', key='wsdm')

all_data.isnull().sum()

all_data_no_na = all_data.copy()
all_data_no_na.replace(["NaN", 'NaT'], np.nan, inplace = True)
all_data_no_na = all_data_no_na.dropna()
all_data_no_na.isnull().sum()

display(all_data_no_na[:10])
len(all_data_no_na)

# test_data = all_data.loc[all_data['target'].isnull()]
# train_data = all_data.loc[all_data['target'].isnull()==False]

# test_data.isnull().sum()

# train_data.isnull().sum()

# # y = all_data['target']
# # X = all_data.drop(['target'], axis = 1)

# real_test_X = test_data.drop(['target'], axis = 1)

# y = train_data[['target']]
# X = train_data.drop(['target'], axis = 1)

# train_X, test_X, train_y, test_y = train_test_split(X,y,test_size=0.4,random_state=1)
# test_X, val_X, test_y, val_y = train_test_split(test_X,test_y,test_size=0.5,random_state=1)

#creat dataset from all_data_no_na
y = all_data_no_na[['target']]
X = all_data_no_na.drop(['target'], axis = 1)

train_X, test_X, train_y, test_y = train_test_split(X,y,test_size=0.4,random_state=1)
test_X, val_X, test_y, val_y = train_test_split(test_X,test_y,test_size=0.5,random_state=1)

ratio_1 = np.sum(train_y[train_y['target'] == 1]) / len(train_y)
print(ratio_1)

print(len(train_X),len(train_y))
print(len(val_X),len(val_y))
print(len(test_X),len(test_y))

#add tiny data for debugging
train_tiny_X = train_X[:10000]
train_tiny_y = train_y[:10000]
train_tiny_X.to_csv('music_data/train_tiny_X.csv')
train_tiny_y.to_csv('music_data/train_tiny_Y.csv')
display(train_tiny_y)

# train_data.to_csv('music_data_raw/train_data_updated.csv')
# test_data.to_csv('music_data_raw/test_data_updated.csv')

#real_test_X.to_csv('music_data/real_test_X_no_label.csv')
train_X.to_csv('music_data/train_X.csv')
test_X.to_csv('music_data/test_X.csv')
val_X.to_csv('music_data/valid_X.csv')
train_y.to_csv('music_data/train_Y.csv')
test_y.to_csv('music_data/test_Y.csv')
val_y.to_csv('music_data/valid_Y.csv')