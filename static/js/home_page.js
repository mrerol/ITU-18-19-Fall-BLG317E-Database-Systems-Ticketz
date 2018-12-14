expeditions = [];




$('#from').on('change', function () {

    let value = this.value;
    $('#from_ter').empty();
    $.ajax({
        data : {
            city_id: value
        },
        type: "POST",
        url: "get_city_of_terminal_with_city_id/" + value
    }).done(function (data) {
        $('#from_ter').append(' <option disabled selected value="*">Select To ter</option>')
        for( i = 0; i<data.length; i++){
            console.log(data[i][0])
            $('#from_ter').append(' <option value="' + data[i][0] + '">' + data[i][1] +'</option>')
        }
        //$('#from_ter').
    })
});


$('#to').on('change', function () {

    let value = this.value;
    $('#to_ter').empty();
    $.ajax({
        data : {
            city_id: value
        },
        type: "POST",
        url: "get_city_of_terminal_with_city_id/" + value
    }).done(function (data) {
        $('#to_ter').append(' <option disabled selected value="*">Select To ter</option>')
        for( i = 0; i<data.length; i++){
            console.log(data[i][0])
            $('#to_ter').append(' <option value="' + data[i][0] + '">' + data[i][1] +'</option>')
        }
        //$('#from_ter').
    })
});