//获取URL中的某个参数
function getUrlParameter(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return decodeURI(r[2]);
    return null;
}

//修改或添加url中某个参数的值
//有就修改,没有就添加
function setUrlParameter(url, name, value) {
    var re = new RegExp(name + "=[^&]*", "gim");
    var m = re.test(url);
    // console.log(m)
    //有这个参数,修改参数即可
    if (m) return url.replace(re, name + '=' + value);
    //没有这个参数
    else {
        //判断是否已有其他参数
        // console.log(url)
        // console.log(url.indexOf('?'))
        if (url.indexOf('?') < 0) return url +'?' + name + '=' + value;
        else return url + '&' + name + '=' + value;
    }
}

//checkbox的全选和反选
function CheckAllToggle($checkall, checkboxs) {

    //var all_obj_checkbox = $("input[_tag='obj_checkbox']");
    var all_obj_checkbox = $("input[" + checkboxs + "]");
    // .checked 可以之间获取checkbox的状态
    //console.log($checkall.checked)

    if ($checkall.checked) {
        all_obj_checkbox.prop('checked', true)
    }
    else {
        all_obj_checkbox.prop('checked', false)
    }


}


//打开新的layerIframe
function layer_iframe(title, url) {
    layer.full(
        layer.open({
            type: 2,
            title: title,
            shadeClose: false,
            // shade: true,
            shade: [0.5],
            maxmin: true, //开启最大化最小化按钮
            area: ['auto', 'auto'],
            content: url
            , cancel: function (index, layero) {
                if (confirm('确定要关闭么,未提交的数据将不会保存')) { //只有当点击confirm框的确定时，该层才会关闭
                    layer.close(index)
                }
                return false;
            }

        }))
}


//选择一个用户
function select_a_user(text, callback) {
    //返回的方法名:
    layer.open({
        type: 2,
        title: text,
        shadeClose: false,
        // shade: true,
        shade: [0.5],
        // maxmin: true, //开启最大化最小化按钮
        area: ['950px', '600px'],
        content: '/hr/layer_select_hr?js_callback=' + callback,
    })
    console.log("回调函数名:" + callback)
}


//我的require
function my_require() {


    var $obj = $(".my_require")
    var flag = 1
    $.each($obj, function (i, v) {
        $v = $(v)
        if (!$.trim($v.val())) {
            //存在没填的
            // $v.focus()
            // layer.tips('我是另外一个tips，只不过我长得跟之前那位稍有些不一样。', $v, {
            //     tips: [1, '#3595CC'],
            //     time: 4000
            // });
            layer.tips('此为必填项', $v);
            // layer.msg("请完整填该信息")
            flag = 0
            return false
        }
    })

    if (flag == 1) return true
    else return false

}


//判断某参数是否在数组中
function in_array(stringToSearch, arrayToSearch) {
    for (s = 0; s < arrayToSearch.length; s++) {
        thisEntry = arrayToSearch[s].toString();
        if (thisEntry == stringToSearch) {
            return true;
        }
    }
    return false;
}

//从字符串中取出数字
get_num_from_str = function () {
    //var reg = /\d+/g;
    //var str = v.name;
    // var ms = str.match(reg)
}

