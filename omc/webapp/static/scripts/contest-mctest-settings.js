$(document).ready(function() {
    function updateMCSettings() {
        $.ajax({
            url: updateUrl + '?id=' + contestId,
            type: 'POST',
            data: {
                use_mc_test: $('#use-mctest').prop('checked') == true,
                mc_test_time: $('#mctest-time').val(),
                mc_test_questions: $('#mctest-questions').val(),
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                if (response.success) {
                    $('#mctest-alert-frame').html('<div class="custom-alerts alert alert-success" role="alert"><button type="button" class="close" data-dismiss="alert" aria-hidden="true"></button>Cập nhật thông tin thành công</div>');
                } else {
                    $('#mctest-alert-frame').html('<div class="custom-alerts alert alert-danger" role="alert"><button type="button" class="close" data-dismiss="alert" aria-hidden="true"></button>Cập nhật thông tin không thành công</div>');
                }
            }
        });
    }

    $('#btn-update-mctest').on('click', function(e) {
        e.preventDefault();
        updateMCSettings();
    });
});
