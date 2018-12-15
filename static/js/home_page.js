expeditions = [];
var q = new Date();
var m = q.getMonth()+1;
var d = q.getDate();
var y = q.getFullYear();


$(document).ready(function() {
    $('.datepicker').datepicker({});

    len = $('#hidden_expedition').val()
    while(i< len){
        console.log(i)
        console.log(len)
        if($('#expedition-'+ i).val() != ""){
            i++
            expeditions.push($('#expedition-'+ j).val())

        }
        j++
    }

}).on('change', function(){
    tempDay = $('#date').val().split('/')
    if(tempDay[2]<y){
        document.getElementById("date").style.borderColor = "red";
        alert('please pick a valid day')
        $('#date').val("")
    }
    else if(tempDay[2] ==y ){
        if(tempDay[0]<m){
            document.getElementById("date").style.borderColor = "red";
            alert('please pick a valid day')
            $('#date').val("")
        }
        else if(tempDay[0] ==m ){
            if(tempDay[1]<d){
                document.getElementById("date").style.borderColor = "red";
                alert('please pick a valid day')
                $('#date').val("")
            }
            else{
                $('.datepicker').hide();
                let value = $('#date').val()
                $('#js_date').val(value);
                document.getElementById("date").style.borderColor = "";
            }
        }
        else{
            $('.datepicker').hide();
            let value = $('#date').val()
            $('#js_date').val(value);
            document.getElementById("date").style.borderColor = "";
        }
    }
    else{
        $('.datepicker').hide();
        let value = $('#date').val()
        $('#js_date').val(value);
        document.getElementById("date").style.borderColor = "";
    }



});


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
        $('#from_ter').append(' <option disabled selected value="*">Select From Terminal</option>')
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
        $('#to_ter').append(' <option disabled selected value="*">Select To Terminal</option>')
        for( i = 0; i<data.length; i++){
            console.log(data[i][0])
            $('#to_ter').append(' <option value="' + data[i][0] + '">' + data[i][1] +'</option>')
        }
        //$('#from_ter').
    })
});
