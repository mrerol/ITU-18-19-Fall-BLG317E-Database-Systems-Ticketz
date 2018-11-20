
function add()
{

    deneme = true
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
    if ($('#city').val()==""){
        document.getElementById("city").style.borderColor = "red";
        deneme = false

    }
    if ($('#address').val()==""){
        document.getElementById("address").style.borderColor = "red";
        deneme = false
    }
    if ($('#phone').val()==""){
        document.getElementById("phone").style.borderColor = "red";
        deneme = false
    }
    if ($('#website').val()==""){
        document.getElementById("website").style.borderColor = "red";
        deneme = false
    }

    if(deneme)
        document.getElementById("add_hotel").submit();
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

