console.log('Hello from acpm.js!');

const graph = new graphology.Graph();

document.addEventListener("DOMContentLoaded", () => {

    const loadMetroData = fetch('./Version1/metro.txt')
        .then(response => response.text())
        .then(text => {
            const lines = text.split('\n');
            for (const line of lines) {
                if (line.startsWith('V')) {
                    const [_, node, name, lineNum] = line.split(';');
                    console.log(parseInt(node), name, lineNum);
                    graph.addNode(parseInt(node), { label: name, x: 0, y:0 ,line: parseInt(lineNum) });
                } else if (line.startsWith('E')) {
                    const [_, node1, node2, time] = line.split(';');
                    console.log(node1, node2, time);
                    graph.addEdge(parseInt(node1), parseInt(node2), { time: parseInt(time) });
                }
            }
        })
        .catch(error => {
            console.error('Error fetching or processing metro.txt:', error);
        });

    // Update the nodes with x,y position with fetch('pospoints.txt')
    const loadPositions = fetch('./Version1/pospoints.txt')
        .then(response => response.text())
        .then(text => {
            const lines = text.split('\n');
            for (const line of lines) {
                const [node, x, y] = line.split(' ');
                graph.mergeNodeAttributes(parseInt(node), { x: parseFloat(x), y: parseFloat(y) });
            }
        })
        .catch(error => {
            console.error('Error fetching or processing pospoints.txt:', error);
        });

    // Ensure both fetches are done before rendering the graph
    Promise.all([loadMetroData, loadPositions]).then(() => {
        // Instantiate sigma.js and render the graph
        const container = document.getElementById('graph');
        const sigmaInstance = new Sigma(graph, container);
    });

});
