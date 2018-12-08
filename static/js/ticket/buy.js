$('input[type="checkbox"]').on('change', function() {
    $('input[name="' + this.name + '"]').not(this).prop('checked', false);
});


function add()
{

    let deneme = true
    console.log(document.querySelectorAll('input[type="checkbox"]:checked').length )
    if (document.querySelectorAll('input[type="checkbox"]:checked').length == 0){
        document.getElementById("plane").style.borderColor = "red";
        deneme = false;
    }

    if(deneme){
        document.getElementById("add_ticket").submit()
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
