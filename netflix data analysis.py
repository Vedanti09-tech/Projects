# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1okEF1mTnMF8Y57X0MlM9VP4qNU8IFeua
"""



import numpy as np
import pandas as pd
import plotly.express as px
from textblob import TextBlob

df=pd.read_csv('netflix_titles.csv')



df.shape

df.head()

df.columns

x=df.groupby(["rating"]).size().reset_index(name="counts")
print(x)

pieChart=px.pie(x,values="counts",names='rating',title='Distribution of content on Netflix')
pieChart.show()

df['director']=df['director'].fillna('Director not specified')
df.head()

director_list=pd.DataFrame()
print(director_list)

director_list=df['director'].str.split(',',expand=True).stack()
print(director_list)

director_list=director_list.to_frame()
print(director_list)

director_list.columns=['Directors']
print(director_list)

directors=director_list.groupby(['Directors']).size().reset_index(name='Total Count')
print(directors)

directors=directors[directors.Directors!='Diretor not specified']
print(directors)

directors=directors.sort_values(by=['Total Count'], ascending=False)
print(directors)

topDirectors=directors.head()
print(topDirectors)

barchart=px.bar(topDirectors,x='Total Count',y='Directors',title='Top 5 Directors on NetFlix')
barchart.show()

topDirectors=topDirectors.sort_values(by=['Total Count'])
barchart=px.bar(topDirectors,x='Total Count',y='Directors',title='Top 5 Directors on NetFlix')
barchart.show()

"""#Analyzing the top 5 Actors on Netflix"""

df['cast']=df['cast'].fillna('Cast not specified')
cast_df=pd.DataFrame()
cast_df=df['cast'].str.split(',',expand=True).stack()
cast_df=cast_df.to_frame()
cast_df.columns=['Actor']
actors=cast_df.groupby(['Actor']).size().reset_index(name='Total Count')
actors=actors[actors.Actor!='Cast not specified']
actors=actors.sort_values(by=['Total Count'],ascending=False)
top5Actors=actors.head()
top5Actors=top5Actors.sort_values(['Total Count'])
bargraph=px.bar(top5Actors,x='Total Count',y='Actor',title='Top 5 actors on Netflix')
bargraph.show()

"""#Analyzing the content produced on netflix based on years"""

df1=df[['type','release_year']]
df1=df1.rename(columns={'release_year':"Release Year",'type':'Type'})
df2=df1.groupby(['Release Year','Type']).size().reset_index(name='Total Count')

df2=df2[df2['Release Year']>2000]
graph=px.line(df2,x='Release Year',y='Total Count',color='Type',title='Trend of Content produced on Netflix every year')
graph.show()

"""#Sentiment Analysis of Netflix Content"""

df3=df[['release_year','description']]
df3=df3.rename(columns={'release_year':'Release Year','description':'Description'})
for index,rows in df3.iterrows():
  d=rows['Description']
  testimonial=TextBlob(d)
  p=testimonial.sentiment.polarity
  if p==0:
    sent ="Neutral"
  elif p>0:
    sent='Positive'
  else:
    sent='Negative'
  df3.loc[[index,2],'Sentiment']=sent
df3=df3.groupby(['Release Year','Sentiment']).size().reset_index(name="Total Count")
df3=df3[df3['Release Year']>2005]
barGraph=px.bar(df3,x='Release Year',y='Total Count',color='Sentiment',title='Sentiment Analysis of Content on Netflix')
barGraph.show()