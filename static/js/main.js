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
            count = res.length;
            text = "共完成" + count + "人";
            if (count > 0) {
                text += ",分别为:";
                for (let i of res) {
                    text += '<br>' + i;
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