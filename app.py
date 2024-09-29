from flask import Flask, render_template, request, jsonify
import numpy as np
import random
from kmeans import KMeans




app = Flask(__name__)




# Generate a random dataset
def generate_random_data(n_samples=300, n_features=2):
    return np.random.rand(n_samples, n_features).tolist()




data = generate_random_data()




@app.route('/')
def index():
    return render_template('index.html')




@app.route('/data')
def get_data():
    return jsonify(data)




@app.route('/run_kmeans', methods=['POST'])
def run_kmeans():
    global data
    method = request.json.get('method')
    n_clusters = request.json.get('n_clusters', 3)  # Use the passed number of clusters
    if not method:
        return jsonify({"error": "No method provided"}), 400




    kmeans = KMeans(n_clusters=n_clusters, init_method=method)
    centroids, labels = kmeans.fit(np.array(data))




    return jsonify({"centroids": centroids.tolist(), "labels": labels.tolist(), "data": data})




@app.route('/generate_dataset', methods=['POST'])
def generate_dataset():
    global data
    data = generate_random_data()
    return jsonify(data)




@app.route('/reset', methods=['POST'])
def reset():
    global data
    data = generate_random_data()  # Generate a new random dataset
    return jsonify(data)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)









