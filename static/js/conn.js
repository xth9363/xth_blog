/*nav*/
$(function () {
    $(".nav>li").hover(function () {
        $(this).children('ul').stop(true, true).show(400);
    }, function () {
        $(this).children('ul').stop(true, true).hide(400);
    })
});




/*search*/


//
$(function () {
    $("#searchform").on('submit', function () {
        // alert("提交")
        var keys = $("#keyboard").val();
        if (!$.trim(keys)) return false
        // console.log("搜索")
    })

    $(".search_ico").click(function () {
        $(".search_bar").toggleClass('search_open');
        var keys = $("#keyboard").val();
        if ($.trim(keys)) {
            $("#searchform").submit();
        } else {
            return false;
        }
    });
});

/*banner*/
$(function () {
    $('#ban').easyFader();
});

