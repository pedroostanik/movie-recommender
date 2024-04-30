from sqlalchemy import create_engine, sql
import pandas as pd
import os
import logging
import socket
import psycopg2

# 179.225.130.214

class MyDataBase():    

    def __init__(self):   

        # ratings_path = os.path.join(os.path.dirname(__file__), '../../data/processed/ratings.csv')
        # movies_path = os.path.join(os.path.dirname(__file__), '../../data/processed/movies.csv')

        # self.ratings = pd.read_csv(ratings_path)
        # self.movies = pd.read_csv(movies_path)
        # self.movies.set_index('movieId')
        # self.ratings.set_index('userId')

        # self.ratings.rename(columns={'movieId': 'itemid'}, inplace=True)
        # self.ratings.rename(columns={'userId': 'userid'}, inplace=True)
        # print(f"### self.ratings {self.ratings}")
        # self.ratings = self.ratings[["userid", "itemid", "rating"]]

        # self.movies = self.movies.rename(columns={'movieId': 'itemid'})
        
        logging.basicConfig(level=logging.DEBUG)

         # Obtém o nome do host
        hostname = socket.gethostname()
        # Obtém o endereço IP associado ao nome do host
        local_ip = socket.gethostbyname(hostname)
        print(f'LOCAL IP:{local_ip}') 
        logging.debug(f'LOCAL IP: {local_ip}')

        # DB_USER = os.environ.get('DB_USER')
        # DB_PASSWORD = os.environ.get('DB_PASSWORD')
        ###NEW        
        self.DB_USER = os.environ.get('DB_USER')
        self.DB_PASSWORD = os.environ.get('DB_PASSWORD')
        self.DB_USER = "master-user"
        self.DB_PASSWORD = "master-user"
        self.DB = "app-recomendacao" 
        self.DB_HOST = "34.136.46.250"    
        
        
        DB_CONNECTION = f'postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB}'

        self.conn = create_engine(DB_CONNECTION)      


        
    def getRatings(self):
        # self.ratings.to_sql('ratings', self.conn, if_exists='append', index=False)
        ratings = pd.read_sql("SELECT * FROM ratings", self.conn)

        # # Estabelecendo a conexão
        # connection = mysql.connector.connect(
        #     user=self.DB_USER,
        #     password=self.DB_PASSWORD,
        #     database=self.DB,
        #     host=self.DB_HOST
        # )

        # # Consulta SQL
        # sql_query = "SELECT * FROM ratings"

        # # Executando a consulta SQL e carregando os resultados em um DataFrame
        # ratings = pd.read_sql_query(sql_query, connection)

        # # Fechando a conexão
        # connection.close()
        return ratings

    def getMovies(self):
        # self.movies.to_sql('movies', self.conn, if_exists='append', index=False)
        movies = pd.read_sql("SELECT * FROM movies", self.conn)

        # # Estabelecendo a conexão
        # connection = mysql.connector.connect(
        #     user=self.DB_USER,
        #     password=self.DB_PASSWORD,
        #     database=self.DB,
        #     host=self.DB_HOST
        # )

        # # Consulta SQL
        # sql_query = "SELECT * FROM movies"

        # # Executando a consulta SQL e carregando os resultados em um DataFrame
        # movies = pd.read_sql_query(sql_query, connection)

        # Fechando a conexão
        # connection.close()
        return movies
    
    def insert_rating(self, item_id, rating, user_exit, user_id):
        if (not user_exit):
            result = pd.read_sql("SELECT MAX(CAST(userid AS INTEGER)) AS max_valor FROM ratings", self.conn)
            max_user = str(int(result.iloc[0, 0]) + 1)
        else:
            max_user = str(user_id)
        item_id = str(item_id)
        rating = float(rating)
        print(f'max_user: {max_user}')
        print(f'item_id: {item_id}')
        print(f'rating: {rating}')

        # connection = self.conn.connect()
        # connection.execute(f"INSERT INTO ratings (userid, itemid, rating) VALUES ('{max_user}', '{item_id}', {rating})")
        # connection.commit()  # Commit para salvar as mudanças no banco de dados
        # print("Dados inseridos com sucesso!")


        ####

        # Conectar ao banco de dados
        conn = psycopg2.connect(
            dbname="app-recomendacao",
            user="master-user",
            password="master-user",
            host="34.136.46.250"
        )

        # Criar um cursor
        cur = conn.cursor()

        # Executar a operação de inserção
        try:
            cur.execute("INSERT INTO ratings (userid, itemid, rating) VALUES (%s, %s, %s)", (max_user, item_id, rating))
            conn.commit()  # Commit para salvar as mudanças no banco de dados
            print("Dados inseridos com sucesso!")
        except psycopg2.Error as e:
            print("Erro ao inserir dados:", e)
            conn.rollback()  # Rollback em caso de erro
        finally:
            # Fechar o cursor e a conexão
            cur.close()
            conn.close()




