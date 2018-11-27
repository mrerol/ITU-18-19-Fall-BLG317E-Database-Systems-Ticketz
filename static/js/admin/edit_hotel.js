
    let image_count = 0

    function deleteImage(i) {
        console.log(i)
        $('#i'+i).remove()
    }

    function imageAdd() {
        image_count ++;
        a = '<div class="input-group-prepend" id="i' +image_count +'">' +
            '                                        <div class="input-group"><span class="input-group-text">' +
            '                                            <i class="far fa-images"></i>' +
            '                                        </span>\n' +
            '                                    </div>\n' +
            '                                    <label for="image' + image_count +'" hidden></label><input type="file" name="image' + image_count + '" accept="image/*" />\n' +
            '                                    <span class="input-group-text">\n' +
            '                                        <i onclick="imageAdd()" class="fas fa-plus"></i>\n' +
            '                                    </span> ' +
            '                                   <span class="input-group-text">' +
            '                                       <i onclick="deleteImage(' + image_count + ')" class="fas fa-minus"></i>' +
            '                                   </span></div>'

        $('#images').append(a)
    }

    $(document).ready(function () {

        $('#js_hotel_name').val($('#hotel_name').val());
        $('#js_e_mail').val($('#e_mail').val());
        $('#js_address').val($('#address').val());
        $('#js_city').val($('#city').val());
        $('#js_phone').val($('#phone').val());
        $('#js_description').val($('#description').val());
        $('#js_website').val($('#website').val());




    });



    function edit()
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
            document.getElementById("edit_hotel").submit()
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


