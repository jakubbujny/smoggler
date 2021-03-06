$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

$.getJSON( "/config-data", function( data ) {
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
    $('#submit').addClass("hide")
    $('#button-spinner').removeClass("hide")
    let minutesToWaitBetweenMeasurements = 5
    if ($('#inputFastMode').is(":checked")) {
        minutesToWaitBetweenMeasurements = 1
    }
    let queueSize = $('#inputHistoryLength').val() * 60 / minutesToWaitBetweenMeasurements
    $.ajax('/config-save', {
        data: JSON.stringify({"minutesToWaitBetweenMeasurements": minutesToWaitBetweenMeasurements, "queueSize": queueSize}),
        contentType: 'application/json',
        type: 'POST',
        success: function () {
            $("#submit").addClass("btn-success").val("Saved!")
            setTimeout(function () {
                $("#submit").removeClass("btn-success").val("Save")
            }, 5000)
            $('#submit').removeClass("hide")
            $('#button-spinner').addClass("hide")
        },
        error: function () {
            $("#submit").addClass("btn-danger").val("Failure!")
            setTimeout(function () {
                $("#submit").removeClass("btn-danger").val("Save")
            }, 5000)
            $('#submit').removeClass("hide")
            $('#button-spinner').addClass("hide")
        }
    })
})
