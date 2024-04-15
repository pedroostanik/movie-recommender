from flask import Flask, jsonify, request
import flask_basicauth
from ..models.movie_recommender import MovieRecommender as MR

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'conik'
app.config['BASIC_AUTH_PASSWORD'] = '12345678'

basic_auth = flask_basicauth.BasicAuth(app)

columns = ["movieId", "rating"]

@app.route('/moviesList')
def movies_list():
    movieRec = MR()
    list = movieRec.show_movies()
    df_dict = list.to_dict(orient='records')
    return jsonify(df_dict)

@app.route('/indicateMovie/<userId>', methods = ['GET'])
@basic_auth.required
def indicate_movies(userId):
    # dados = request.get_json()    
    movieRec = MR()
    indicated_movies = movieRec.execute(userId)
    indicated_movies_dict = indicated_movies.to_dict(orient='records')
    return jsonify(indicated_movies_dict)

@app.route('/avaliateMovie', methods = ['POST'])
def avaliate_movie():
    dados = request.get_json()
    movieRec = MR() 
    movieRec.insert_ratings(dados)
    return "success"

    
app.run(debug=True, host='0.0.0.0')