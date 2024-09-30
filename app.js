// Function to plot data and centroids
async function plotData(centroids = [], labels = []) {
    const data = await fetchData();
    const colors = labels.map(label => getColorForCluster(label));

    const trace1 = {
        x: data.map(point => point[0]),
        y: data.map(point => point[1]),
        mode: 'markers',
        type: 'scatter',
        name: 'Data Points', 
        marker: {
            size: 10,
            color: colors,
            opacity: 0.8
        }
    };

    const trace2 = {
        x: centroids.map(centroid => centroid[0]),
        y: centroids.map(centroid => centroid[1]),
        mode: 'markers',
        type: 'scatter',
        name: 'Centroids', 
        marker: {
            size: 12,
            color: 'red',
            symbol: 'cross'
        }
    };

    const layout = {
        title: 'KMeans Clustering',
        xaxis: { title: 'X-axis' },
        yaxis: { title: 'Y-axis' }
     
    };

    Plotly.newPlot('plot', [trace1, trace2], layout);
}
