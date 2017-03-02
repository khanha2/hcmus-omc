$(document).ready(function() {
    var writingTestQuestionsFiles;

    function alertSuccess() {
        $('#writingtest-alert-frame').html('<div class="custom-alerts alert alert-success" role="alert"><button type="button" class="close" data-dismiss="alert" aria-hidden="true"></button>Cập nhật thông tin thành công</div>');
    }

    function alertDanger() {
        $('#writingtest-alert-frame').html('<div class="custom-alerts alert alert-danger" role="alert"><button type="button" class="close" data-dismiss="alert" aria-hidden="true"></button>Cập nhật thông tin không thành công</div>');
    }

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

    function loadWritingQuestions() {
        function addWritingQuestion(element) {
            var row = '<div class="panel panel-default"><div class="panel-body"><p>' + element.content + '</p></div></div>';
            $('#writing-questions').append(row);
        }

        $.ajax({
            url: questionsUrl,
            type: 'GET',
            data: {
                id: contestId,
                type: 'wt'
            },
            success: function(response) {
                $('#writing-questions').empty();
                $(response).each(function(index, element) {
                    addWritingQuestion(element);
                });
            }
        });
    }

    function uploadWritingQuestions() {
        var data = new FormData($('#form-upload-writingtest-questions').get(0));
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
                    loadWritingQuestions();
                } else {
                    alertDanger();
                }
            },
            error: function(response, error) {
                alertDanger();
            }
        });
    }

    $('#file-writingtest-questions').on('change', function(e) {
        writingTestQuestionsFiles = e.target.files;
    });

    $('#btn-update-writing-questions').on('click', function(e) {
        e.preventDefault();
        uploadWritingQuestions();
    });

    $('#btn-update-writingtest').on('click', function(e) {
        e.preventDefault();
        updateWritingTestSettings();
    });

    loadWritingQuestions();
});
