from sqlalchemy import create_engine
import pandas as pd
import os
import logging
import socket
import mysql.connector

# 179.225.130.214

class MyDataBase():    

    def __init__(self):   
        logging.basicConfig(level=logging.DEBUG)

        #  # Obtém o nome do host
        # hostname = socket.gethostname()
        # # Obtém o endereço IP associado ao nome do host
        # local_ip = socket.gethostbyname(hostname)
        # print(f'LOCAL IP:{local_ip}') 
        # logging.debug(f'LOCAL IP: {local_ip}')

        # DB_USER = os.environ.get('DB_USER')
        # DB_PASSWORD = os.environ.get('DB_PASSWORD')

        # logging.debug(f'DB_USER: {DB_USER}')
        # logging.debug(f'DB_PASSWORD: {DB_PASSWORD}')
        
        
        # DB_CONNECTION = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB}'
        # self.conn = create_engine(DB_CONNECTION)   


        ###NEW        
        self.DB_USER = os.environ.get('DB_USER')
        self.DB_PASSWORD = os.environ.get('DB_PASSWORD')
        self.DB = "app-recomendacao" 
        self.DB_HOST = "34.123.119.20"        


        
    def getRatings(self):
        # ratings = pd.read_sql("SELECT * from ratings", self.conn)

        # Estabelecendo a conexão
        connection = mysql.connector.connect(
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            database=self.DB,
            host=self.DB_HOST
        )

        # Consulta SQL
        sql_query = "SELECT * FROM ratings"

        # Executando a consulta SQL e carregando os resultados em um DataFrame
        ratings = pd.read_sql_query(sql_query, connection)

        # Fechando a conexão
        connection.close()
        return ratings

    def getMovies(self):
        # movies = pd.read_sql("SELECT * from movies", self.conn)

        # Estabelecendo a conexão
        connection = mysql.connector.connect(
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            database=self.DB,
            host=self.DB_HOST
        )

        # Consulta SQL
        sql_query = "SELECT * FROM movies"

        # Executando a consulta SQL e carregando os resultados em um DataFrame
        movies = pd.read_sql_query(sql_query, connection)

        # Fechando a conexão
        connection.close()
        return movies
