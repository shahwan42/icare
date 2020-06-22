/*global $ */
/*eslint-env browser*/

$(document).ready(function () {
    $(".side-nav .aside-control span.minus").click(function () {
        $(this).hide().siblings().show();
        $(this).parent().parent().parent().addClass("sidbar");
    });
    $(".side-nav .aside-control span.plus").click(function () {
        $(this).hide().siblings().show();
        $(this).parent().parent().parent().removeClass("sidbar");
    });

    $(".aside_list ul li").click(function () {
        $(this).addClass("active").siblings().removeClass("active");
    });
    if ($(window).width() < 576) {
        $(".page-body-wrapper").addClass("sidbar");
    }

});
$(document).ready(function () {
    $('#table_id').DataTable();
});


function getCustomFields() {
    console.log("GOT CALLED")
    dropdown = $("select")
    console.log(dropdown.children("option:selected").val())
    pk = dropdown.children("option:selected").val()
    $.ajax({
        type: "get",
        url: `/lists/${pk}/custom_fields`,
        data: "data",
        dataType: "application/json",
        success: function (response) {
            console.log(response.data)
        },
        error: function (error) {
            console.log(error)
        }
    });
}
