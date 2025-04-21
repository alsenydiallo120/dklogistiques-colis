
$(document).ready(function(){
    $('#id_employes').change(function () {
        id=$(this).val()
        $.ajax({
            method: "GET",
            url: "detail/"+id+'/',
            data: $(this).val(),
            dataType: "json",
            success: function (success) {
                console.log(success)
            },
            error: function (response) {
                console.log(response)
            }
        });
    })
})
