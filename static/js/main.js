$('#appendFormSubmit').click(function () {
    content = $('#appendForm-content').val();
    if (content === "") {
        alert("content不能为空");
        return;
    }
    $.post('/notifications/append',
        {
            content: content
        },
        function () {
            window.location.reload();
        });
});

function toggleCollapse(id, nf_id) {
    let that = $("#collapse" + id);
    if (that.hasClass("in")) {
        that.collapse("hide");
        return;
    }
    $(".collapse.in").collapse('hide');
    that.collapse('toggle');
    $.ajax({
        type: 'POST',
        url: '/notifications/detail/' + nf_id,
        complete: function (data, status) {
            if (status !== 'success') {
                that.html("<h4>" + data.responseJSON.msg + "</h4>");
                return false
            }
            res = data.responseJSON.res;
            text = "";
            if (res.checked.length > 0) {
                text += "共完成" + res.checked.length + "人";
                text += ",分别为:";
                for (let i of res.checked) {
                    text += '<br>' + i.username + ' ' + i.nickname;
                }
            }
            if (res.unchecked.length > 0) {
                text += "<br>未完成" + res.unchecked.length + "人";
                text += ",分别为:";
                for (let i of res.unchecked) {
                    text += '<br>' + i.username + ' ' + i.nickname;
                }
            }
            that.html("<h4>" + text + "</h4>");
        }
    })
}

function checkNf(nf_id) {
    $.ajax({
        type: 'POST',
        url: '/notifications/check/' + nf_id,
        complete: function (data, status) {
            if (status !== 'success') {
                $.toast({
                    heading: data.responseJSON.msg,
                    position: 'top-center',
                    loader: false,
                    icon: 'error'
                });
                return false
            }
            window.location.reload()
        }
    })
}