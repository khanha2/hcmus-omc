$(document).ready(function() {
    function updateWritingTestSettings() {
        $.ajax({
            url: updateUrl + '?id=' + contestId,
            type: 'POST',
            data: {
                use_writing_test: $('#use-writingtest').prop('checked') == true,
                writing_test_time: $('#writingtest-time').val(),
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                if (response.success) {
                    $('#writingtest-alert-frame').html('<div class="custom-alerts alert alert-success" role="alert"><button type="button" class="close" data-dismiss="alert" aria-hidden="true"></button>Cập nhật thông tin thành công</div>');
                } else {
                    $('#writingtest-alert-frame').html('<div class="custom-alerts alert alert-danger" role="alert"><button type="button" class="close" data-dismiss="alert" aria-hidden="true"></button>Cập nhật thông tin không thành công</div>');
                }
            }
        });
    }

    $('#btn-update-writingtest').on('click', function(e) {
        e.preventDefault();
        updateWritingTestSettings();
    });
});
