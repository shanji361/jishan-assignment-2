async function fetchData() {
    const response = await fetch('/data');
    const data = await response.json();
    return data;
}




async function fetchCentroids(method, nClusters) {
    const response = await fetch('/run_kmeans', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ method: method, n_clusters: nClusters }),
    });
    const result = await response.json();
    return result;
}




function getColorForCluster(clusterIndex) {
    const colors = [
        "rgb(93, 164, 214)", // Cluster 1
        "rgb(255, 144, 14)", // Cluster 2
        "rgb(44, 160, 101)", // Cluster 3
        "rgb(255, 65, 54)",  // Cluster 4
        "rgb(55, 65, 54)"    // Cluster 5
    ];
    return colors[clusterIndex % colors.length]; // Cycle through colors if more clusters than colors
}




async function plotData(centroids = [], labels = []) {
    const data = await fetchData(); // Fetch current data points




    // Map labels to colors for the data points
    const colors = labels.map(label => getColorForCluster(label));




    const trace1 = {
        x: data.map(point => point[0]),
        y: data.map(point => point[1]),
        mode: 'markers',
        type: 'scatter',
        marker: {
            size: 10,
            color: colors, // Use assigned colors for clusters
            opacity: 0.8
        }
    };




    const trace2 = {
        x: centroids.map(centroid => centroid[0]),
        y: centroids.map(centroid => centroid[1]),
        mode: 'markers',
        type: 'scatter',
        marker: {
            size: 12,
            color: 'red',
            symbol: 'cross'
        },
        name: 'Centroids'
    };




    const layout = {
        title: 'KMeans Clustering',
        xaxis: { title: 'X-axis' },
        yaxis: { title: 'Y-axis' }
    };




    Plotly.newPlot('plot', [trace1, trace2], layout);
}




async function generateNewDataset() {
    await fetch('/generate_dataset', { method: 'POST' });
    plotData(); // Update the plot after generating the new dataset
}




async function stepThrough() {
    const nClusters = document.getElementById('num_clusters').value;
    const method = document.getElementById('init_method').value;




    const result = await fetchCentroids(method, nClusters);
    const centroids = result.centroids;
    const labels = result.labels;




    // Plot data points
    await plotData(centroids, labels);
}




async function runToConvergence() {
    const nClusters = document.getElementById('num_clusters').value;
    const method = document.getElementById('init_method').value;




    let currentCentroids = [];
    let currentLabels = [];




    for (let i = 0; i < nClusters; i++) { // Run KMeans for the specified number of times
        const result = await fetchCentroids(method, nClusters);
        currentCentroids = result.centroids;
        currentLabels = result.labels;




        await plotData(currentCentroids, currentLabels);
        await new Promise(resolve => setTimeout(resolve, 1000)); // Wait 1 second between iterations
    }
}




// Function to reset to original data points
async function resetAlgorithm() {
    await generateNewDataset(); // Re-generate the dataset
    plotData(); // Re-plot the original data
}




// Call plotData when the page loads
document.addEventListener('DOMContentLoaded', plotData);









