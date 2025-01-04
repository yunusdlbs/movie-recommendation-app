import pandas as pd

data=pd.read_csv('dataset.csv')
# data.head()
# data.describe()
# data.isnull().sum()
# data.info()
# data.columns
movies=data[['id', 'title', 'overview', 'genre']]
# print(movies)
# Featue Selection
movies['tags']=movies['overview']+movies['genre']
new_data=movies.drop(columns=['overview', 'genre'])
from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=10000, stop_words='english')
myvector=cv.fit_transform(new_data['tags'].values.astype('U')).toarray()

from sklearn.metrics.pairwise import cosine_similarity
similarity=cosine_similarity(myvector)
a=new_data[new_data['title']=='The Godfather'].index[0]


# for i in a[:5]:
#     print(new_data.iloc[i[0]].title)
# def recommand(movie):
#     index=new_data[new_data['title']==movie].index[0]
#     distance=sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
#     for i in distance[:5]:
#         print(new_data.iloc[i[0]].title)    

#recommand('Iron Man')
#print(a[:5])

import pickle
# pickle.dump(new_data, open('movie_list.pckl', 'wb'))
pickle.dump(similarity, open('similarity.pckl', 'wb'))
# a=pickle.load(open('movie_list.pckl', 'rb'))
# print(a)