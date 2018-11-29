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
    var output = document.getElementById('logo');
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

function deleteImage(i) {
    console.log(i)
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
    if ($('#hotel_name').val()==""){
        document.getElementById("hotel_name").style.borderColor = "red";
        deneme = false

    }
    if ($('#e_mail').val()==""){
        document.getElementById("e_mail").style.borderColor = "red";
        deneme = false
    }
    if ($('#description').val()==""){
        document.getElementById("description").style.borderColor = "red";
        deneme = false
    }
    /*if ($('#city').val()==""){
        document.getElementById("city").style.borderColor = "red";
        deneme = false

    }*/
    if ($('#address').val()==""){
        document.getElementById("address").style.borderColor = "red";
        deneme = false
    }
    if ($('#phone').val()==""){
        document.getElementById("phone").style.borderColor = "red";
        deneme = false
    }
    /*if ($('#website').val()==""){
        document.getElementById("website").style.borderColor = "red";
        deneme = false
    }*/

    if(deneme){
        $('#s').val(image_count)
        document.getElementById("add_hotel").submit()
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

$('#hotel_name').on('change keyup paste delete', function () {

    let value = this.value;
    $('#js_hotel_name').val(value);
    document.getElementById("hotel_name").style.borderColor = "";

});

$('#e_mail').on('change keyup paste delete', function () {

    let value = this.value;
    $('#js_e_mail').val(value);
    document.getElementById("e_mail").style.borderColor = "";

});

$('#description').on('change keyup paste delete', function () {

    let value = this.value;
    $('#js_description').val(value);
    document.getElementById("description").style.borderColor = "";

});

$('#city').on('change keyup paste delete', function () {

    let value = this.value;
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

$('#website').on('change keyup paste delete', function () {

    let value = this.value;
    $('#js_website').val(value);
    document.getElementById("website").style.borderColor = "";

});

