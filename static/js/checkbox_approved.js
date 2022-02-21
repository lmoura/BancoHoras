function checkClick(chkId) {
    checked = ""
    if($("#approved_" + chkId).is(":checked")) {
        checked = true;
    } else {
        checked = false;
    }

    $.ajax({
        url: "update_chk",
        type: "get",
        data: {
            chkid: chkId,
            ischecked: checked},
        success: function (result,status,xhr) {
            $("#textData").html(result);
        }
    });
}