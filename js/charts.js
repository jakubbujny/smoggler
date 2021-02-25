function CreatePMChart(pmName, pmMeasurements, labels, referenceValue, renderContainerID) {
    let reference = []

    for (let i = 0; i < pmMeasurements.length; i++) {
        reference.push(referenceValue)
    }

    new Chart(document.getElementById(renderContainerID).getContext('2d'), {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'WHO safe limit',
                    type: "line",
                    borderColor: 'rgb(255, 0, 0)',
                    backgroundColor: 'rgba(0, 0, 0, 0.0)',
                    data: reference
                },
                {
                    label: 'PM '+pmName,
                    type: "line",
                    backgroundColor: 'rgb(175, 175, 175)',
                    data: pmMeasurements
                }
            ]
        },
        options: {
            scales: {
                xAxes: [{
                    ticks: {
                        suggestedMin: 0,
                        suggestedMax: 10,
                        maxTicksLimit: 10,
                        fontSize: 20
                    }
                }]
            },
            title: {
                display: true,
                text: 'PM '+pmName,
                fontSize: 16,
                fontColor: (pmMeasurements[pmMeasurements.length - 1] > referenceValue) ? "#F00" : "#000"
            }
        }
    });
}

function CreatePMGauge(pmMeasurements, pmName, renderContainerID, safeLimit) {
    google.charts.load('current', {'packages':['gauge']});
    google.charts.setOnLoadCallback(function() {

        let data = google.visualization.arrayToDataTable([
            ['Label', 'Value'],
            ['PM '+pmName, pmMeasurements[pmMeasurements.length - 1]],
        ]);
        let options = {
            greenFrom:0,
            greenTo: safeLimit,
            redFrom: safeLimit,
            redTo: 999,
            minorTicks: 5,
            max: 100
        };
        let chart = new google.visualization.Gauge(document.getElementById(renderContainerID));
        chart.draw(data, options);
        $(window).resize(function(){
            chart.draw(data, options);
        });
    });
    
}

export {CreatePMChart, CreatePMGauge}
