from flask import Flask, jsonify, request
import flask_basicauth
import sys
import os

# Adiciona o diretório 'src' ao caminho de busca de módulos do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Agora você pode importar o módulo 'movie_recommender.py' normalmente
# from src.models.movie_recommender import MovieRecommender as MR
from src.models.surprise_recommender import SurpriseRecommender as SR

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

print(f"USERNAME: {app.config['BASIC_AUTH_USERNAME']}")

basic_auth = flask_basicauth.BasicAuth(app)

columns = ["movieId", "rating"]

@app.route('/')
def core():
    return "My automatic API!"

@app.route('/moviesList')
def movies_list():
    movieRec = SR()
    list = movieRec.show_movies()
    df_dict = list.to_dict(orient='records')
    return jsonify(df_dict)

@app.route('/indicateMovie/<userId>', methods = ['GET'])
@basic_auth.required
def indicate_movies(userId):
    # dados = request.get_json()    
    movieRec = SR()
    indicated_movies = movieRec.execute_knn(userId)
    # indicated_movies_dict = indicated_movies.to_dict(orient='records')
    # return jsonify(indicated_movies_dict)
    return indicated_movies

@app.route('/avaliateMovie', methods = ['POST'])
def avaliate_movie():
    dados = request.get_json()
    # movieRec = MR() 
    # movieRec.insert_ratings(dados)
    return "success"

@app.route('/indicateMovieByMovie/<movieId>', methods = ['GET'])
@basic_auth.required
def indicate_movie_by_movie(movieId):
    # movieRec = MR()
    # indicated_movies = movieRec.indicate_movie_by_movie(movieId)
    # indicated_movies = indicated_movies.to_dict(orient='records')
    # return jsonify(indicated_movies)
    return ""

@app.route('/insertUser/<movieId>/<rating>', methods = ['GET'])
def insert_user_rating(movieId, rating, user_exist=False, user_id=None):
    user_exist = request.args.get('userExit', False)  # Obtém o valor de userExit da query string ou False se não estiver presente
    user_id = request.args.get('userId', None)   
    movieRec = SR()
    movieRec.new_rating(movieId, rating, user_exist, user_id)


    
app.run(debug=True, host='0.0.0.0')