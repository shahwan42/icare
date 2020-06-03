/*global $ */
/*eslint-env browser*/

$(document).ready(function () {
    $(".side-nav .aside-control span.minus").click(function (){
       $(this).hide().siblings().show();
        $(this).parent().parent().parent().addClass("sidbar");
    });
    $(".side-nav .aside-control span.plus").click(function (){
       $(this).hide().siblings().show();
        $(this).parent().parent().parent().removeClass("sidbar");
    });
    
    $(".aside_list ul li").click(function () {
       $(this).addClass("active").siblings().removeClass("active"); 
    });
	if ($(window).width() < 576){
		$(".page-body-wrapper").addClass("sidbar");
	}
    
});
$(document).ready( function () {
    $('#table_id').DataTable();
});


