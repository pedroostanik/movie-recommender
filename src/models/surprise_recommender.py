from surprise import SVD, BaselineOnly, Dataset, Reader, KNNBasic
from surprise.model_selection import cross_validate
import pandas as pd
import os
import sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from data.database.my_data_base import MyDataBase

class SurpriseRecommender():

    def __init__(self):
        
        # ratings_path = os.path.join(os.path.dirname(__file__), '../../data/raw/ratings.csv')
        # self.ratings = pd.read_csv(ratings_path)       

        # movies_path = os.path.join(os.path.dirname(__file__), '../../data/raw/movies.csv')
        # self.movies = pd.read_csv(movies_path)   

        db = MyDataBase()
        self.ratings = db.getRatings()
        self.movies = db.getMovies()    

        self.reader = Reader(rating_scale=(1,5))

    def execute(self):
        reader = Reader(rating_scale=(1,5))

        ### ADDING A NEW USER ###
        df_new = pd.DataFrame({
            "userId": [700, 700, 700, 700],
            "movieId": [1196, 260, 1210, 2628],
            "rating": [5, 4.5, 5, 5],
            "timestamp": [datetime.timestamp(datetime.now()),datetime.timestamp(datetime.now()),datetime.timestamp(datetime.now()),datetime.timestamp(datetime.now())]
        })        

        self.ratings = pd.concat([self.ratings, df_new])
        self.ratings.reset_index(drop=True, inplace=True)

        print("### MY DF ###")
        print(self.ratings)

        ### ADDING A NEW USER ###   

        data = Dataset.load_from_df(self.ratings[["userId", "movieId", "rating"]], reader=reader)        
        print(f'data: {data.df}')   

        train_set = data.build_full_trainset()

        model = SVD()
        cv_results = cross_validate(model, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

        # Print the average RMSE and MAE scores
        print('Average RMSE:', cv_results['test_rmse'].mean())
        print('Average MAE:', cv_results['test_mae'].mean())  


        

        # Obtenha os itens que o usuário já classificou
        inner_uid = train_set.to_inner_uid(700)
        itens_classificados_pelo_usuario = train_set.ur[inner_uid]
        print(f'itens_classificados_pelo_usuario: {itens_classificados_pelo_usuario}')

        all_itens = set(range(train_set.n_items))

        # Itens que o usuário ainda não classificou
        itens_nao_classificados_pelo_usuario = all_itens - set([j for (j, _) in itens_classificados_pelo_usuario])

        # Criar um conjunto de teste contendo as classificações ausentes do usuário
        teste_usuario_x = [(train_set.to_raw_uid(inner_uid), train_set.to_raw_iid(item_id), 3) for item_id in itens_nao_classificados_pelo_usuario]

        # Fazer previsões para as classificações ausentes do usuário
        previsoes_usuario_x = model.test(teste_usuario_x)

        # Ordenar as previsões em ordem decrescente de classificação
        previsoes_ordenadas = sorted(previsoes_usuario_x, key=lambda x: x.est, reverse=True)

        # Obter as 10 melhores previsões
        top_10_previsoes = previsoes_ordenadas[:10]

        movies_list = []
        # Exibir as 10 melhores previsões
        for previsao in top_10_previsoes:
            print(f'Item: {previsao.iid}, Previsão de Classificação: {previsao.est}')
            movie_title = self.movies.query(f'movieId=={previsao.iid}')['title'].iloc[0]
            movies_list.append(movie_title)

        return movies_list
    
    def show_movies(self):
        return self.movies
    
    def execute_knn(self, t_user, n_recommendations=10):        
        print(f'self ratings: {self.ratings}')
        self.data = Dataset.load_from_df(self.ratings[["userid", "itemid", "rating"]], self.reader)
        train_set = self.data.build_full_trainset()        

        # Obtenha os itens que o usuário já classificou
        try:
            inner_uid = train_set.to_inner_uid(t_user)
        except: 
            return f"The user {t_user} doesn't exist. Please, use the endpoint to insert a new user!"

        itens_classificados_pelo_usuario = train_set.ur[inner_uid]

        model = KNNBasic()
        cv_results = cross_validate(model, self.data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

        # Print the average RMSE and MAE scores
        print('Average RMSE:', cv_results['test_rmse'].mean())
        print('Average MAE:', cv_results['test_mae'].mean()) 

        # Passo 1: Obtenha os itens que o usuário já avaliou
        user_items = self.data.raw_ratings
        user_items = [(uid, iid, r) for (uid, iid, r, _) in user_items if uid == t_user]

        # Passo 2: Crie um conjunto contendo todos os itens disponíveis
        all_items = set(range(train_set.n_items))

        # Itens que o usuário ainda não classificou
        itens_nao_classificados_pelo_usuario = all_items - set([j for (j, _) in itens_classificados_pelo_usuario])

        # Criar um conjunto de teste contendo as classificações ausentes do usuário
        teste_usuario_x = [(train_set.to_raw_uid(inner_uid), train_set.to_raw_iid(item_id), 3) for item_id in itens_nao_classificados_pelo_usuario]

        # Fazer previsões para as classificações ausentes do usuário
        previsoes_usuario_x = model.test(teste_usuario_x)

        # Ordenar as previsões em ordem decrescente de classificação
        previsoes_ordenadas = sorted(previsoes_usuario_x, key=lambda x: x.est, reverse=True)

        # Obter as 10 melhores previsões
        top_n_predictions = previsoes_ordenadas[:n_recommendations]

        movies_list = []
        for previsao in top_n_predictions:
            print(f'Item: {previsao.iid}, Previsão de Classificação: {previsao.est}')
            movie_title = self.movies.query(f'itemid=={previsao.iid}')['title'].iloc[0]
            movies_list.append(movie_title)

        return movies_list  
    
    
    def new_rating(self, itemId, rating, user_exit, user_id):

        mdb = MyDataBase()
        mdb.insert_rating(itemId, rating, user_exit, user_id)

        # user_df = pd.DataFrame({"userId": new_id_user,
        #                         "movieId": itemId,
        #                         "rating": rating
        #                         })
        # new_df = pd.concat([old_df, user_df])


        # self.data = Dataset.load_from_df(new_df[["userId", "movieId", "rating"]], self.reader)  
        # model = KNNBasic()
        # cv_results = cross_validate(model, self.data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

        # # Print the average RMSE and MAE scores
        # print('Average RMSE:', cv_results['test_rmse'].mean())
        # print('Average MAE:', cv_results['test_mae'].mean()) 





