$(function () {
    //验证车牌
    var $plate = $("#p_name");

    $plate.change(function () {

        var plate = $plate.val().trim();

        if (!plate) {
            $("#pname_info").html("车牌不能为空").css("color", 'red');
        } else {
            $("#pname_info").html("");
        }

        if (plate.length) {
            //    将车牌发送给服务器进行校验
            $.getJSON('/vehicle/checkplate/', {'plate': plate}, function (data) {

                console.log(data);

                var $username_info = $("#username_info");

                if (data['status'] === 200) {
                    $username_info.html("新车牌").css("color", 'green');
                    var obj = document.getElementById("username_select");
                    obj.options.length = 0;
                    for (var i = 0; i < data['username'].length; i++) {
                        obj.add(new Option(data['username'][i], '1'));
                    }
                } else if (data['status'] === 901) {
                    $username_info.html("车牌已存在").css("color", 'red');
                    var obj = document.getElementById("username_select");
                    obj.options.length = 0;
                    // obj.add(new Option('4', '4'));
                    obj.add(new Option(data['username'], data['uid']));
                }
            })
        }
    })

    //道路限制提示

})