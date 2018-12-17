
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
        document.getElementById("edit_driver").submit()
    }
    else{
            $(".message-box-danger-length").toggle(750, function () {
                setTimeout(function () {
                    $(".message-box-danger-length").toggle(750);
                }, 2500);
            });

   }

}


