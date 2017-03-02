$(document).ready(function() {
    var mctestQuestionsFiles;

    function alertSuccess() {
        $('#mctest-alert-frame').html('<div class="custom-alerts alert alert-success" role="alert"><button type="button" class="close" data-dismiss="alert" aria-hidden="true"></button>Cập nhật thông tin thành công</div>');
    }

    function alertDanger() {
        $('#mctest-alert-frame').html('<div class="custom-alerts alert alert-danger" role="alert"><button type="button" class="close" data-dismiss="alert" aria-hidden="true"></button>Cập nhật thông tin không thành công</div>');

    }

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
                    alertSuccess();
                } else {
                    alertDanger();
                }
            },
            error: function(response, error) {
                alertDanger();
            }
        });
    }

    function loadMCQuestions() {
        function addMCQuestion(index, element) {
            var row = '<div class="panel panel-default"><div class="panel-body"><strong>Câu hỏi ' + (index + 1) + ':</strong><p>' + element.content + '</p><ol type="A"><li>' + element.a + '</li><li>' + element.b + '</li><li>' + element.c + '</li><li>' + element.d + '</li></ol>Đáp án: <strong>' + element.answer + '</strong></div></div>';
            $('#mc-questions').append(row);
        }

        $.ajax({
            url: questionsUrl,
            type: 'GET',
            data: {
                id: contestId,
                type: 'mc'
            },
            success: function(response) {
                $('#mc-questions').empty();
                $(response).each(function(index, element) {
                    addMCQuestion(index, element);
                });
            }
        });
    }

    function uploadMCQuestions() {
        var data = new FormData($('#form-upload-mctest-questions').get(0));
        $.ajax({
            url: uploadQuestionsUrl + '?id=' + contestId,
            type: 'POST',
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    alertSuccess();
                    loadMCQuestions();
                } else {
                    alertDanger();
                }
            },
            error: function(response, error) {
                alertDanger();
            }
        });
    }

    $('#file-mctest-questions').on('change', function(e) {
        mctestQuestionsFiles = e.target.files;
    });

    $('#btn-update-mc-questions').on('click', function(e) {
        e.preventDefault();
        uploadMCQuestions();
    });

    $('#btn-update-mctest').on('click', function(e) {
        e.preventDefault();
        updateMCSettings();
    });

    loadMCQuestions();
});
