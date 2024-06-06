const station = {
    id: 11, //int, "numero de la station"
    stationName: "Place d'Italie", //string
    ligneNumber: 7, //positive int
    isTerminus: False, //boolean
    liaisons: [
            {
                num_AutreSommet: 12, //int
                temps: 5, //positive int, le temps de marche entre
            }
        ]//dict of "liaison" objects - 
    }

console.log(myObject);