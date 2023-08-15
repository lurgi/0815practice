from flask import Flask, render_template,jsonify
from pymongo import MongoClient, DESCENDING, ASCENDING

client = MongoClient('localhost', 27017)
db = client.jungle

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

#좋아요 순으로 정렬한 영화
@app.route("/movies/sort_like",methods = ["GET"])
def moviesSortedLike():
    movies = list(db.movies.find({"deleted" : False},{"_id" : False}).sort("open_year", ASCENDING))
    return jsonify({"ok" : True, "movies" : movies})
#누적관객수
@app.route("/movies/sort_view",methods = ["GET"])
def moviesSortedView():
    movies = list(db.movies.find({"deleted" : False},{"_id" : False}).sort("open_year", ASCENDING))
    return jsonify({"ok" : True, "movies" : movies})
#개봉일순
@app.route("/movies/sort_open",methods = ["GET"])
def moviesSortedOpen():
    movies = list(db.movies.find({"deleted" : False},{"_id" : False}).sort("open_year", ASCENDING))
    return jsonify({"ok" : True, "movies" : movies})
#휴지통
@app.route("/movies/sort_deleted",methods = ["GET"])
def moviesSortedDeleted():
    movies = list(db.movies.find({"deleted" : False},{"_id" : False}).sort("open_year", ASCENDING))
    return jsonify({"ok" : True, "movies" : movies})

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)