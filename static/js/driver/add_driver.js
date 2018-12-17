
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

    if($('#driver_name').val().length < 5 || $('#driver_name').val().length > 20 ){
        document.getElementById("driver_name").style.borderColor = "red";
        value_length = false;
    }
    else
        document.getElementById("driver_name").style.borderColor = "green";

    if (($('#e_mail').val().length < 5 || $('#e_mail').val().length > 20 )){
        document.getElementById("e_mail").style.borderColor = "red";
        value_length = false;
    }
    else
        document.getElementById("e_mail").style.borderColor = "green";

    if (($('#phone').val().length < 5 || $('#phone').val().length > 20 )){
        document.getElementById("phone").style.borderColor = "red";
        value_length = false;
    }
    else
        document.getElementById("phone").style.borderColor = "green";

    if(fill && value_length){
        document.getElementById("add_driver").submit()
    }
    else{
            $(".message-box-danger-length").toggle(750, function () {
                setTimeout(function () {
                    $(".message-box-danger-length").toggle(750);
                }, 2500);
            });

   }

}

$('#driver_name').on('change keyup paste delete', function () {

    let value = this.value;
    $('#js_driver_name').val(value);
    document.getElementById("driver_name").style.borderColor = "";

});

$('#e_mail').on('change keyup paste delete', function () {

    let value = this.value;
    $('#js_e_mail').val(value);
    document.getElementById("e_mail").style.borderColor = "";

});

$('#gender').on('change keyup paste delete', function () {

    let value = this.value;
    $('#js_gender').val(value);
    document.getElementById("gender").style.borderColor = "";

});

$('#city').on('change keyup paste delete', function () {

    let value = $('#city')[0].selectedOptions[0].innerHTML
    $('#js_city').val(value);
    document.getElementById("city").style.borderColor = "";

});



$('#address').on('change keyup paste delete', function () {

    let value = this.value;
    $('#js_address').val(value);
    document.getElementById("address").style.borderColor = "";

});

$('#phone').on('change keyup paste delete', function () {

    let value = this.value;
    $('#js_phone').val(value);
    document.getElementById("phone").style.borderColor = "";

});


