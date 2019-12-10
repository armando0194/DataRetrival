from flask import Flask, jsonify
from flask import request
from flask import abort

from handler.scrapper import ExploitDBScrapper
from handler.indexer import Indexer
from handler.ranker import Ranker


app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

ranker = Ranker()

@app.route('/api/v1.0/recomms/', methods=['GET'])
def get_tasks():
    if not request.json or not 'query' in request.json:
        abort(400)

    tf_idf_res = ranker.query_tf_idf(request.json['query'])
    centroids_res = ranker.query_centroids(request.json['query'])
    return jsonify({'td_idf': tf_idf_res, "centroids": centroids_res})

if __name__ == '__main__':
    app.run(debug=True)