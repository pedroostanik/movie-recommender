import pandas as pd
import numpy as np
import pickle
import os

class MovieRecommender():

    def __init__(self):
        ratings_path = os.path.join(os.path.dirname(__file__), '../../data/raw/ratings.csv')
        movies_path = os.path.join(os.path.dirname(__file__), '../../data/raw/movies.csv')

        self.ratings = pd.read_csv(ratings_path)
        self.movies = pd.read_csv(movies_path)
        self.movies.set_index('movieId')
        self.ratings.set_index('userId')


    def execute(self, id_user, number_of_equals=10, rating_filter=4, max_number_of_movies=10):
        id_user = int(id_user)
        user_exist = id_user in self.ratings['userId'].values
        if (user_exist):
            return self.indicate_movie(id_user, number_of_equals, rating_filter, max_number_of_movies)
        else:
            return self.blank_recomendation()
        
    def blank_recomendation(self):
        return self.ratings.sort_values('rating', ascending=False).drop(columns=['timestamp']).set_index('userId').head(10)
    
    def show_movies(self):
        return self.movies
    
    def insert_ratings(self, params):
        new_df = pd.DataFrame(params,columns=["userId", "movieId", "rating"])
        self.ratings = pd.concat([self.ratings, new_df])

        self.ratings.to_csv('ratings.csv', index=False)
        with open('dataframe.pkl', 'wb') as f:
            pickle.dump(self.ratings, f)
    

    def difference_between_users(self, user_a, user_b):
        matriz_a = self.ratings.query(f"userId=={user_a}").sort_values("movieId")[["movieId", 'rating']].set_index('movieId')
        matriz_b = self.ratings.query(f"userId=={user_b}").sort_values("movieId")[["movieId", 'rating']].set_index('movieId')
        gathered_matriz = matriz_a.join(matriz_b, lsuffix="_left",rsuffix="_right").dropna()
        diff = gathered_matriz['rating_left'] - gathered_matriz['rating_right']
        pitag = np.linalg.norm(diff)
        return pitag


    def general_difference(self, target_user):
        users = self.ratings['userId'].unique()
        raw_data = [[target_user, user, self.difference_between_users(target_user, user)] for user in users]
        new_data = pd.DataFrame(raw_data, columns=['id_a', 'id_b', 'distance']).set_index('id_b')
        new_data.sort_values('distance', inplace=True)
        new_data.drop(target_user, inplace=True)
        return new_data

    def indicate_movie(self, target_user, number_of_equals=10, rating_filter=4, max_number_of_movies=10):

        #movies that I've watch
        movies_ive_watch = self.ratings.query('userId==1')['movieId']

        #For the id, we take all movies about this person, less that the common movies!
        new_data = self.general_difference(target_user)

        #ajustar aqui para pegar o primeiro valor, id do usuario
        my_equals = new_data.head(number_of_equals).index
        movies_that_my_equal_liked = self.ratings.set_index('userId').loc[my_equals].query(f'rating>{rating_filter}').sort_values('rating', ascending=False)

        #Treating by mean and orded
        apparition = movies_that_my_equal_liked.groupby('movieId').count()['rating']
        mean = movies_that_my_equal_liked.groupby('movieId').mean()[['rating']]

        movies_that_my_equal_liked = mean.join(apparition, lsuffix='_media_dos_usuarios', rsuffix='_aparicoes_nos_usuarios')
        final_movies = movies_that_my_equal_liked.sort_values(by=['rating_media_dos_usuarios', 'rating_aparicoes_nos_usuarios'], ascending=False)
        final_movies = final_movies.join(self.movies.set_index('movieId')).dropna()
        return final_movies.drop(movies_ive_watch, errors='ignore').head(max_number_of_movies)

    def indicate_movie_by_movie(self, movie_id, number_of_equals=10):
        movie_genre = self.movies.query(f"movieId=={movie_id}")['genres'].iloc[0]
        movies_by_equals = self.ratings.query(f"movieId=={movie_id}").sort_values('rating', ascending=False)
        movies_by_equals = movies_by_equals.head(number_of_equals)['userId'].to_list()

        new_df = pd.DataFrame(columns=['userId', 'movieId', 'rating', 'timestamp'])
        for id in movies_by_equals:
            temp_df = self.ratings.query(f'userId=={id}')            
            new_df = pd.concat([new_df, temp_df])
        new_df = new_df.sort_values('rating', ascending=False)
        new_df = new_df.groupby('movieId').mean()[['rating']]
        gathered_df = self.movies.set_index('movieId').join(new_df, lsuffix="_left",rsuffix="_right").dropna()
        gathered_df = gathered_df.query(f"genres=='{movie_genre}'")
        return gathered_df



    
new_user = [
    {
        "movieId": 4896,
        "rating": 4,
    },
    {
        "movieId": 5816,
        "rating": 4.2,
    },
    {
        "movieId": 81834,
        "rating": 5,
    },
    {
        "movieId": 95170,
        "rating": 2,
    },  
    ]

if (__name__ == "__main__"):
    mr = MovieRecommender()
    # print(mr.execute(11111))
    print(mr.indicate_movie_by_movie(1))