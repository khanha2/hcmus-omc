$(document).ready(function() {
    function loadOverviewTab() {
        $('#contest-from-time').datetimepicker({ format: "DD/MM/YYYY hh:mm" });
        $('#contest-to-time').datetimepicker({ format: "DD/MM/YYYY hh:mm" });

        $('#contest-short-desc').summernote({ height: 150 });
        $('#contest-desc').summernote({ height: 150 });
    }

    function updateOverviewInfo() {
        $.ajax({
            url: updateUrl + '?id=' + contestId,
            type: 'POST',
            data: {
                name: $('#contest-name').val(),
                from_time: $('#contest-from-time input').val(),
                to_time: $('#contest-to-time input').val(),
                short_description: $('#contest-short-desc').val(),
                description: $('#contest-desc').val(),
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                if (response.success) {
                    $('#overview-alert-frame').html('<div class="custom-alerts alert alert-success" role="alert"><button type="button" class="close" data-dismiss="alert" aria-hidden="true"></button>Cập nhật thông tin thành công</div>');
                } else {
                    $('#overview-alert-frame').html('<div class="custom-alerts alert alert-danger" role="alert"><button type="button" class="close" data-dismiss="alert" aria-hidden="true"></button>Cập nhật thông tin không thành công</div>');
                }
            }
        });
    }

    $('#btn-update-overview').on('click', function(e) {
        e.preventDefault();
        updateOverviewInfo();
    });

    loadOverviewTab();
});
