const graph = new graphology.Graph();

document.addEventListener('DOMContentLoaded', function() {
    console.log("Hello, World!");

    fetch('http://127.0.0.1:8000/stations', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())  // Convertir la réponse en JSON
    .then(data => {
        console.log(data);  // Afficher les données JSON dans la console
        renderGraph(data);  // Appeler la fonction pour afficher le graphe
    })
    .catch(error => {
        console.error('Error fetching stations:', error);
    });

    function renderGraph(data) {
        // Créer une instance de Sigma.js

        // Ajouter les nœuds au graphe
        data.forEach(station => {

            console.log(station);
            graph.addNode(station["id"], { label: station["stationName"], x: station["x"], y: station["y"], size: 10, color: "black" });
        });


    }

});

const sigmaInstance = new sigma(graph, container = document.getElementById('graph'));

