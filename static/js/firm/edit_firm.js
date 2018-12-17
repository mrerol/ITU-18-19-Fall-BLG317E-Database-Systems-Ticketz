let image_count = 0
var loadImage = function(event, i) {
    var output = document.getElementById('images'+i);
    if(event.target.files.length != 0){
        output.src = URL.createObjectURL(event.target.files[0]);
        output.class = "img-thumbnail";
        output.style = "height: 40%; width: 40%;";
    }
    else{
        output.src = "";
        output.class = "";
        output.style = "";
    }
    };


var loadFile = function(event) {
var output = document.getElementById('logo_image');
    if(event.target.files.length != 0){
        output.src = URL.createObjectURL(event.target.files[0]);
        output.class = "img-thumbnail";
        output.style = "height: 40%; width: 40%;";
    }
    else{
        output.src = "";
    }
};

let image_count = 0

function clicked() {
    $('#logo_image').hide()
}

function deleteImage(i) {
$('#i'+i).remove()

$('#images'+i).hide()
}

function imageAdd() {
    image_count ++;
    a = '<div class="input-group-prepend" id="i' +image_count +'">' +
    '                                        <div class="input-group"><span class="input-group-text">' +
    '                                            <i class="far fa-images"></i>' +
    '                                        </span>' +
    '                                    </div>' +
    '                                    <label for="image' + image_count +'" hidden></label><img id="images'+ image_count+ '" ><input onchange="loadImage(event, ' + image_count +')" type="file" name="image' + image_count + '" accept="image/*" />' +
    '                                    <span onclick="imageAdd()"  class="input-group-text">\n' +
    '                                        <i class="fas fa-plus"></i>\n' +
    '                                    </span> ' +
    '                                   <span onclick="deleteImage(' + image_count + ')" class="input-group-text">' +
    '                                       <i  class="fas fa-minus"></i>' +
    '                                   </span></div>'

    $('#images').append(a)
}


function edit()
{
    /*
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
*/
    let fill = true;
    let value_length = true;

    if($('#firm_name').val().length < 5 || $('#firm_name').val().length > 20 ){
        document.getElementById("firm_name").style.borderColor = "red";
        value_length = false;
    }
    else
        document.getElementById("firm_name").style.borderColor = "green";

    if (($('#password').val().length < 5 || $('#password').val().length > 20 )){
        document.getElementById("password").style.borderColor = "red";
        value_length = false;
    }
    else
        document.getElementById("password").style.borderColor = "green";

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
        $('#s').val(image_count)
        document.getElementById("edit_firm").submit()
    }
    else{
            $(".message-box-danger-length").toggle(750, function () {
                setTimeout(function () {
                    $(".message-box-danger-length").toggle(750);
                }, 2500);
            });

   }

}


