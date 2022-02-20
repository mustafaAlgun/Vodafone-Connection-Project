#!/usr/bin/env python
# coding: utf-8

# In[463]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as patches

from IPython.display import GeoJSON
from shapely.geometry import Point, Polygon
import geojsonio
from geojsonio import display
import geopandas as gpd


# In[481]:


province_map = gpd.read_file("limits_IT_provinces.geojson") #read geojson file from github
province_map =province_map[["prov_name","geometry"]] #we only use prov name and geometry
province_map ["centroid"] = province_map.geometry.centroid #find the centroid of all provinces
province_map


# In[482]:


padova_point = province_map.loc[province_map['prov_name'] == 'Padova'] #select padova geolocation
padova_point


# In[483]:


point = padova_point.iat[0,2]


# In[484]:


province_map = province_map.assign(dist_to_padova=province_map.distance(point))
province_map


# In[485]:


#sort by minimum value of distance
province_map =province_map.sort_values(by = 'dist_to_padova', ascending = True)
province_map


# In[489]:


province_5_nearest = province_map.head(5)
province_5_nearest = province_5_nearest.drop(labels=28, axis=0)
province_5_nearest


# In[490]:


#Select the nearest provinces to Padova
province_5_nearest = province_5_nearest.sort_values('dist_to_padova',ascending = True)
province_5_nearest


# In[491]:


#Starting the main part


# In[468]:


#Reading csc files
df_user = pd.read_csv('distinct_users_day.csv', sep=',', encoding='ANSI') 
df_province = pd.read_csv('codici_istat_provincia.csv', sep=',', encoding='ANSI')

#Filtering data with unknown value
df_province = df_province[df_province['COD_PRO']>0]
#Filtering by visitors
df_user_visitors = df_user[df_user['CUST_CLASS']=='visitor']
#Keeping 4 nearest province to padova that counted.
df_province = df_province[(df_province['PROVINCIA']=='Vicenza') | (df_province['PROVINCIA']=='Venezia') | (df_province['PROVINCIA']=='Treviso') | (df_province['PROVINCIA']=='Rovigo')]
#Merge 2 datasets to get all required columns.
df = df_user_visitors.merge(df_province)
#Dropping unneccessary columns.
df = df.drop('PRO_COM', 1)
df = df.drop('COD_REG', 1)
df = df.drop('PROV_SIGLA', 1)
df = df.drop('COD_COUNTRY', 1)
#Sort by number of visitors.
df = df.sort_values('VISITORS', ascending=False)
df


# In[470]:


#Grouping provinces to directions
direction = []
for i in df['PROVINCIA']:
    if i == 'Rovigo':
        direction.append('S')
    elif i == 'Vicenza':
        direction.append('E')
    else:
        direction.append('W')

df['Directions'] = direction
        
df


# In[466]:


#Weekend days,sum and sort of them based on most visitors.
df_Weekend = df[df['DOW'].str.match('Sabato', 'Domenica')]
df_sum_provinces = df_Weekend.groupby(['PROVINCIA']).sum().reset_index()
df_sum_provinces = df_sum_provinces.sort_values('VISITORS',ascending = False)
df_sum_provinces


# In[459]:


#Plotting provinces with most visitors during weekends.
df = pd.DataFrame({'lab':['Venezia', 'Vicenza', 'Treviso', 'Rovigo'], 'val':[94052, 70716, 47520, 28228
]})
ax = df.plot.bar(x='lab', y='val', rot=0)


# In[467]:


df_sum_directions = df_Weekend.groupby(['Directions']).sum().reset_index()
df_sum_directions = df_sum_directions.sort_values('VISITORS',ascending = False)
df_sum_directions


# In[461]:


#Plotting weekend flux, focus on directions.
df = pd.DataFrame({'lab':['W', 'E', 'S'], 'val':[141572, 70716, 28228
]})
ax = df.plot.bar(x='lab', y='val', rot=0)


# In[473]:


df_working = df[(df['DOW'] != 'Sabato') & (df3['DOW'] != 'Domenica') ]
df_sum_working = df_working.groupby(['Directions','DOW', 'PROVINCIA']).sum().reset_index()
df_sum_working


# In[474]:


#Province with most visitors during daily working days.
df_sum_working_p = df_sum_working.groupby(['PROVINCIA', 'Directions']).sum().reset_index()
df_sum_working_p = df_sum_working_p.sort_values('VISITORS',ascending = False)
df_sum_working_p


# In[475]:


#Direction with most numbers of visitors during daily working days
df_sum_working_d = df_working.groupby(['Directions', 'PROVINCIA']).sum().reset_index()
df_sum_working_d = df_sum_working.sort_values('VISITORS',ascending = False)
df_sum_working_d


# In[476]:


#Sum of visitors at daily working days.
df_sum_days = df_sum_working_d.groupby(['PROVINCIA']).sum().reset_index()
df_sum_days
df_sum_days = df_sum_days.sort_values('VISITORS',ascending = False)
df_sum_days


# In[477]:


#Plotting the provinces eith most number of visitors during daily working days.
df = pd.DataFrame({'lab':['Venezia', 'Vicenza', 'Treviso', 'Rovigo'], 'val':[438196, 294252, 220156, 108572,  
]})
ax = df.plot.bar(x='lab', y='val', rot=0)


# In[478]:


#Sum of visitors at daily working days.
df_sum_working_d = df_sum_working_d.groupby(['DOW']).sum().reset_index()
df_sum_working_by_days = df_sum_working_d.sort_values('VISITORS',ascending = False)
df_sum_working_by_days


# In[480]:


#Sum of visitors in daily working days in all provinces, indicates there is not enormous difference between working days.
df = pd.DataFrame({'VISITORS': [223704
 , 219044, 207352, 205680, 205396]},
                  index=['Venerdi', 'Mercoledi', 'Martedi', 'Lunedi', 'Giovedi'])
plot = df.plot.pie(y='VISITORS', figsize=(5, 5))


# In[ ]:




