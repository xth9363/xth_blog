// $(window).load(function(){$("pre").addClass("prettyprint linenums");prettyPrint();}

$(function () {
    // console.log('$("pre").addClass("prettyprint linenums");prettyPrint();')
    //判断是否显示返回键
    $("#b_back").hide()
     if (document.referrer !== '' && document.referrer.indexOf(window.location.host) > -1) {
        //来自于本网站url
         $("#b_back").show()
        // window.location.href = document.referrer;
    }
});
function jump_page() {
    // alert("123")
    const jp = $("#jump_page_page").val()
    // console.log($jp.val())
    const now_path = $("#now_path").val()
    if ($.trim(jp)){
       // console.log( setUrlParameter(now_path,'page',jp))
       window.location.href =setUrlParameter(now_path,'page',jp)
    }
}
//返回键
function backpage() {
            window.location.href = document.referrer;
            window.history.back(-1);
    // var domain = document.domain;
   // var domain = window.location.host;
   // if (document.referrer !== '' && document.referrer.indexOf(domain) > -1) {
        //来自于本网站url
   // }
   // domain = window.location.host;
   // console.log(domain)
   // {#            window.history.back(-1);#
   // }
   // console.log(window.history)

}

