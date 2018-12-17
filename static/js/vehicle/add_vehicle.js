
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


    let fill = true;
    let value_length = true;

    if($('#vehicle_name').val().length < 5 || $('#vehicle_name').val().length > 20 ){
        document.getElementById("vehicle_name").style.borderColor = "red";
        value_length = false;
    }
    else
        document.getElementById("vehicle_name").style.borderColor = "green";

    if (($('#category').val().length < 5 || $('#category').val().length > 20 )){
        document.getElementById("category").style.borderColor = "red";
        value_length = false;
    }
    else
        document.getElementById("category").style.borderColor = "green";

    if (($('#model').val().length < 5 || $('#model').val().length > 20 )){
        document.getElementById("model").style.borderColor = "red";
        value_length = false;
    }
    else
        document.getElementById("model").style.borderColor = "green";

        if (($('#capacity').val().length < 1 || $('#capacity').val().length > 20 )){
        document.getElementById("capacity").style.borderColor = "red";
        value_length = false;
    }
    else
        document.getElementById("capacity").style.borderColor = "green";

    if (($('#production_year').val().length < 1 || $('#production_year').val().length > 20 )){
        document.getElementById("production_year").style.borderColor = "red";
        value_length = false;
    }
    else
        document.getElementById("production_year").style.borderColor = "green";

    if (($('#production_place').val().length < 5 || $('#production_place').val().length > 20 )){
        document.getElementById("production_place").style.borderColor = "red";
        value_length = false;
    }
    else
        document.getElementById("production_place").style.borderColor = "green";



    if(fill && value_length){
        document.getElementById("add_vehicle").submit()
    }
    else{
            $(".message-box-danger-length").toggle(750, function () {
                setTimeout(function () {
                    $(".message-box-danger-length").toggle(750);
                }, 2500);
            });

   }

}

$('#vehicle_name').on('change keyup paste delete', function () {

    let value = this.value;
    $('#js_vehicle_name').val(value);
    document.getElementById("vehicle_name").style.borderColor = "";

});

$('#category').on('change keyup paste delete', function () {

    let value = this.value;
    $('#js_category').val(value);
    document.getElementById("category").style.borderColor = "";

});

$('#model').on('change keyup paste delete', function () {

    let value = this.value;
    $('#js_model').val(value);
    document.getElementById("model").style.borderColor = "";

});

$('#capacity').on('change keyup paste delete', function () {

    let value = this.value;
    $('#js_capacity').val(value);
    document.getElementById("capacity").style.borderColor = "";

});


$('#production_year').on('change keyup paste delete', function () {

    let value = this.value;
    $('#js_production_year').val(value);
    document.getElementById("production_year").style.borderColor = "";

});

$('#production_place').on('change keyup paste delete', function () {

    let value = this.value;
    $('#js_production_place').val(value);
    document.getElementById("production_place").style.borderColor = "";

});

$('#description').on('change keyup paste delete', function () {

    let value = this.value;
    $('#js_description').val(value);
    document.getElementById("description").style.borderColor = "";

});


