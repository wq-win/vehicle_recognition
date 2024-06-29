$(function () {

})

function search() {
    var $search = $("#search");

    var username = $search.val().trim();

    window.location.href = "http://127.0.0.1:8000/user/search/?username=" + username;
}