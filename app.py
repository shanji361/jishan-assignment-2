from flask import Flask, render_template, request, jsonify
import numpy as np
import random
from kmeans import KMeans


app = Flask(__name__)


def generate_random_data(n_samples=300, n_features=2):
    return np.random.rand(n_samples, n_features).tolist()


data = generate_random_data()




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    global data
    if data is None:
        return jsonify({'error': 'Data is not initialized'}), 400

    if isinstance(data, np.ndarray):
        return jsonify(data.tolist())  
    elif isinstance(data, list):
        return jsonify(data)  
    else:
        return jsonify({'error': 'Unsupported data type'}), 500


@app.route('/run_kmeans', methods=['POST'])
def run_kmeans():
    global kmeans
    global data  

  
    if data is None:
        return jsonify({'error': 'Data is not initialized'}), 400

    data = np.array(data)  

    json_data = request.get_json()
    method = json_data.get('method')
    n_clusters = json_data.get('n_clusters')
    manual_centroids = json_data.get('manual_centroids', None)


    kmeans = KMeans(n_clusters=n_clusters, init_method=method)
    centroids, labels = kmeans.fit(data, initial_centroids=manual_centroids)
    
    return jsonify({'centroids': centroids.tolist(), 'labels': labels.tolist()})


@app.route('/generate_dataset', methods=['POST'])
def generate_dataset():
    global data
    data = generate_random_data()
    return jsonify(data)




@app.route('/reset', methods=['POST'])
def reset():
    global data
    data = generate_random_data()  
    return jsonify(data)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)