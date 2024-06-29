$(function () {
    //验证用户名
    var $username = $("#username_input");

    $username.change(function () {

        var username = $username.val().trim();

        if (username.length) {
            //    将用户名发送给服务器进行校验
            $.getJSON('/user/checkuser/', {'username': username}, function (data) {

                console.log(data);

                if (data['status'] === 200) {
                    $("#username_info").html("√").css("color", 'green');
                } else if (data['status'] === 901) {
                    $("#username_info").html("用户名已存在").css("color", 'red');
                }
            })
        }
    })

    //验证密码规范性
    var $password_input = $("#password_input")

    $password_input.change(function () {
        var password = $password_input.val().trim();

        // 最少6位，包括至少1个大写字母，1个小写字母，1个数字，1个特殊字符
        if (password.search(/^.*(?=.{6,})(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%^&*? ]).*$/) !== -1) {
            $("#password_info").html("√").css("color", 'green');
        } else if (!password.length){
            $("#password_info").html("保留原来密码").css("color", 'green');
        }else {
            $("#password_info").html("最少6位，包括至少1个字母，1个数字，1个特殊字符").css("color", 'red');
        }
    })

    //验证邮箱
    var $email_input = $("#email_input");

    $email_input.change(function () {
        var email = $email_input.val().trim();

        if (email.search(/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/) !== -1) {
            $("#email_info").html("√").css("color", 'green');
        } else if (!email.length){
            $("#email_info").html("保留原来邮箱").css("color", 'green');
        }else {
            $("#email_info").html("邮箱格式错误").css("color", 'red');
        }
    })
})

//提交时，检查数据的有效性
function check() {
    //检查用户名有效性
    var info_color = $("#username_info").css('color');
    // console.log(info_color);
    if (info_color === 'rgb(255, 0, 0)') {
        return false
    }

    var $password_input = $("#password_input");
    var password = $password_input.val().trim();
    //把密码用md5加密传输、存储
    $password_input.val(md5(password));

    //检查密码有效性
    var password_info = $("#password_info").css('color');
    if (password_info === 'rgb(255, 0, 0)'){
        return false
    }

    //检查邮箱有效性
    var info_email = $("#email_info").css('color');
    if (info_email === 'rgb(255, 0, 0)'){
        return false
    }

    return true
}