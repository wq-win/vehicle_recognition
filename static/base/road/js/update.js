$(function () {

})

function save() {
    var $rid = $("#rid");
    var $rn = $("#rn");
    var $rr = $("#rr");

    var rid = $rid.val().trim();
    var rn = $rn.val().trim();
    var rr = $rr.val().trim();

    window.location.href = "http://127.0.0.1:8000/vehicle/saveroad/?rid=" + rid + "&rn=" + rn + "&rr=" + rr;
}