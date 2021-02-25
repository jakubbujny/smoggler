import {CreatePMChart, CreatePMGauge} from "./charts.js"

$.getJSON( "/check-version", function( data ) {
    if(data.version === "outdated") {
        $("#version").html("New version available! Visit <a href='https://github.com/jakubbujny/smoggler#how-to-update'>https://github.com/jakubbujny/smoggler#how-to-update</a>")
    }
})

$.getJSON( "/sensor-data", function( data ) {
    let labels = []
    let pm25 = []
    let pm10 = []

    data.measurements.forEach(element => function() {
        labels.push(new Date(element.timestamp*1000).toLocaleTimeString("en-EN"))
        pm25.push(element.pm25)
        pm10.push(element.pm10)
    }())

    $(".loading-spinner-to-delete").remove()

    CreatePMChart("2.5", pm25, labels, 25, "pm25")
    CreatePMGauge(pm25, '2.5', 'pm25_gauge', 25)

    CreatePMChart("10", pm10, labels, 50, "pm10")
    CreatePMGauge(pm10, '10', 'pm10_gauge', 50)
})
