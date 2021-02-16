$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

$.getJSON( "/config-data", function( data ) {
    console.log(data.prod.queueSize)
    console.log(data.prod.minutesToWaitBetweenMeasurements)
    if (data.prod.minutesToWaitBetweenMeasurements === 1) {
        $('#inputFastMode').prop('checked', true);
    } else {
        $('#inputFastMode').prop('checked', false);
    }

    let lengthInHours = (data.prod.queueSize * data.prod.minutesToWaitBetweenMeasurements) / 60
    $(`#inputHistoryLength option[value="${lengthInHours}"]`).attr("selected",true);
    $(".loading-spinner-to-delete").remove()
    $(".hide").removeClass("hide")
})

$('#submit').click(function () {
    console.log()
    console.log()
    let minutesToWaitBetweenMeasurements = 5
    if ($('#inputFastMode').is(":checked")) {
        minutesToWaitBetweenMeasurements = 1
    }
    let queueSize = $('#inputHistoryLength').val() * 60 / minutesToWaitBetweenMeasurements
    console.log(queueSize)
})
