from sqlalchemy import create_engine
import pandas as pd
import os

# 179.225.130.214

class MyDataBase():    

    def __init__(self):   
        DB_USER = os.environ.get('DB_USER')
        DB_PASSWORD = os.environ.get('DB_PASSWORD')
        DB_HOST = "34.123.119.20" 
        DB = "app-recomendacao" 
        DB_CONNECTION = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB}'
        self.conn = create_engine(DB_CONNECTION)       
        
    def getRatings(self):
        ratings = pd.read_sql("SELECT * from ratings", self.conn)
        return ratings

    def getMovies(self):
        movies = pd.read_sql("SELECT * from movies", self.conn)
        return movies
