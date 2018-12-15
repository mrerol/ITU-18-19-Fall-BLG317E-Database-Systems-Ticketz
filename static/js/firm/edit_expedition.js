$('.clockpicker').clockpicker();

var q = new Date();
var m = q.getMonth()+1;
var d = q.getDate();
var y = q.getFullYear();
$(document).ready(function() {
    $('.datepicker').datepicker({});
    id = $('#selected_plane').val()
    category = $('#category' + id).val()
    description = $('#description' + id).val()
    model = $('#model' + id).val()
    capacity = $('#capacity' + id).val()
    $('#hidden_category').val(category)
    $('#hidden_description').val(description)
    $('#hidden_model').val(model)
    $('#hidden_capacity').val(capacity)
    $('#hidden_plane').show()

    $('#js_from').val( $('#from')[0].selectedOptions[0].innerHTML)
    $('#js_to').val( $('#to')[0].selectedOptions[0].innerHTML)
    $('#js_from_ter').val( $('#from_ter')[0].selectedOptions[0].innerHTML)
    $('#js_to_ter').val( $('#to_ter')[0].selectedOptions[0].innerHTML)
    $('#js_dep_time').val( $('#dep_time').val())
    $('#js_arr_time').val( $('#arr_time').val())
    $('#js_date').val( $('#date').val())
    $('#js_price').val( $('#price').val())
    $('#js_plane').val( $('#selected_plane')[0].selectedOptions[0].innerHTML)
    $('#js_driver').val( $('#driver')[0].selectedOptions[0].innerHTML)


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

$('#selected_plane').on('change keyup paste delete', function () {
    id = $('#selected_plane').val()
    category = $('#category' + id).val()
    description = $('#description' + id).val()
    model = $('#model' + id).val()
    capacity = $('#capacity' + id).val()
    $('#hidden_category').val(category)
    $('#hidden_description').val(description)
    $('#hidden_model').val(model)
    $('#hidden_capacity').val(capacity)
    $('#hidden_plane').show()


});

$('#price').on('change delete', function () {

    if($('#price').val()<10)
        $('#price').val(10)
});

$('#from').on('change keyup paste delete', function () {

    let value = $('#from')[0].selectedOptions[0].innerHTML
    $('#js_from').val(value);
    document.getElementById("from").style.borderColor = "";
});

$('#from_ter').on('change keyup paste delete', function () {

    let value = $('#from_ter')[0].selectedOptions[0].innerHTML
    $('#js_from_ter').val(value);
    document.getElementById("from_ter").style.borderColor = "";
});

$('#to').on('change keyup paste delete', function () {

    let value = $('#to')[0].selectedOptions[0].innerHTML
    $('#js_to').val(value);
    document.getElementById("to").style.borderColor = "";

});

$('#to_ter').on('change keyup paste delete', function () {

    let value = $('#to_ter')[0].selectedOptions[0].innerHTML
    $('#js_to_ter').val(value);
    document.getElementById("to_ter").style.borderColor = "";

});

$('#dep_time').on('change', function () {

    let value = $('#dep_time').val()
    $('#js_dep_time').val(value);
    document.getElementById("dep_time").style.borderColor = "";


});

$('#arr_time').on('change', function () {

    let value = $('#arr_time').val()
    $('#js_arr_time').val(value);
    document.getElementById("arr_time").style.borderColor = "";
});



$('#price').on('change', function () {

    let value = $('#price').val()
    $('#js_price').val(value);
    document.getElementById("price").style.borderColor = "";

});


$('#selected_plane').on('change keyup paste delete', function () {

    let value = $('#selected_plane')[0].selectedOptions[0].innerHTML
    $('#js_plane').val(value);
    document.getElementById("selected_plane").style.borderColor = "";

});

$('#driver').on('change keyup paste delete', function () {

    let value = $('#driver')[0].selectedOptions[0].innerHTML
    $('#js_driver').val(value);
    document.getElementById("driver").style.borderColor = "";

});

function add()
{

    var $captcha = $( '#recaptcha' ),
        response = grecaptcha.getResponse();

    if (response.length === 0) {
        $( '.msg-error').text( "reCAPTCHA is mandatory" );
        if( !$captcha.hasClass( "error" ) ){
            $captcha.addClass( "error" );
            return false;
        }
    }
    else {
        $( '.msg-error' ).text('');
        $captcha.removeClass( "error" );
    }

    let deneme = true

    if ($('#from').val()== null){
        document.getElementById("from").style.borderColor = "red";
        deneme = false

    }

    if ($('#from_ter').val()=="" || $('#from_ter').val()== null){
        document.getElementById("from_ter").style.borderColor = "red";
        deneme = false

    }

    if ($('#to').val()==null){
        document.getElementById("to").style.borderColor = "red";
        deneme = false

    }

    if ($('#to_ter').val()=="" || $('#to_ter').val()== null){
        document.getElementById("to_ter").style.borderColor = "red";
        deneme = false

    }

    if ($('#dep_time').val()=="" || $('#dep_time').val()== null) {

        document.getElementById("dep_time").style.borderColor = "red";
        deneme = false
    }


    if ($('#arr_time').val()=="" || $('#arr_time').val()== null){
        document.getElementById("arr_time").style.borderColor = "red";
        deneme = false

    }

    let value = $('#dep_time').val()
    arr = value.split(':')
    if(arr.length != 2){
        document.getElementById("dep_time").style.borderColor = "red";
        deneme = false
    }
    else{
        if(arr[0].length != 2 || arr[0] < '00' || arr[0] > '23' ){
            document.getElementById("dep_time").style.borderColor = "red";
            deneme = false
        }
        else{
            if(arr[1].length != 2 || arr[1] < '00' || arr[1] > '59'){
                document.getElementById("dep_time").style.borderColor = "red";
                deneme = false
            }
        }
    }

    value = $('#arr_time').val()
    arr = value.split(':')
    if(arr.length != 2){
        document.getElementById("arr_time").style.borderColor = "red";
        deneme = false
    }
    else{
        if(arr[0].length != 2 || arr[0] < '00' || arr[0] > '23' ){
            document.getElementById("arr_time").style.borderColor = "red";
            deneme = false
        }
        else{
            if(arr[1].length != 2 || arr[1] < '00' || arr[1] > '59'){
                document.getElementById("arr_time").style.borderColor = "red";
                deneme = false
            }
        }
    }

    value = $('#date').val()
    arr = value.split('/')
    if(arr.length != 3){
        document.getElementById("date").style.borderColor = "red";
        deneme = false
    }
    else{
        if(arr[0].length != 2 || arr[0] < '00' || arr[0] > '12' ){
            document.getElementById("date").style.borderColor = "red";
            deneme = false
        }
        else{
            if(arr[1].length != 2 || arr[1] < '00' || arr[1] > '31'){
                document.getElementById("date").style.borderColor = "red";
                deneme = false
            }
            else{
                if(arr[2].length != 4 || arr[2] < '2018' || arr[2] > '2200'){
                    document.getElementById("date").style.borderColor = "red";
                deneme = false
                }
            }
        }
    }

    tempDay = $('#date').val().split('/')
    if(tempDay[2]<y){
        document.getElementById("date").style.borderColor = "red";
        alert('please pick a valid day')
        deneme = false
    }
    else if(tempDay[2] ==y ){
        if(tempDay[0]<m){
            document.getElementById("date").style.borderColor = "red";
            alert('please pick a valid day')
            deneme = false

        }
        else if(tempDay[0] ==m ){
            if(tempDay[1]<d){
                document.getElementById("date").style.borderColor = "red";
                alert('please pick a valid day')
                deneme = false
            }
        }
    }

    if ($('#price').val()=="" || $('#price').val()== null){
        document.getElementById("price").style.borderColor = "red";
        deneme = false

    }

    if ($('#selected_plane').val()=="" || $('#selected_plane').val()== null){
        document.getElementById("selected_plane").style.borderColor = "red";
        deneme = false

    }

    if ($('#driver').val()=="" || $('#driver').val()== null){
        document.getElementById("driver").style.borderColor = "red";
        deneme = false

    }

    if ($('#to_ter').val()== $('#from_ter').val()){
        document.getElementById("from_ter").style.borderColor = "red";
        document.getElementById("to_ter").style.borderColor = "red";
        deneme = false

    }

    if ($('#arr_time').val() == $('#dep_time').val()){
        document.getElementById("arr_time").style.borderColor = "red";
        document.getElementById("dep_time").style.borderColor = "red";
        deneme = false

    }

    if(deneme){
        document.getElementById("add_expedition").submit()
    }
    else{
        $(".message-box-danger").toggle(750, function () {
            setTimeout(function () {
                $(".message-box-danger").toggle(750);
            }, 2500);
        });


        return false
    }

}

