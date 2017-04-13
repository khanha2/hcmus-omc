$(document).ready(function() {
    function showSuccessAlert() {
        $('#alert-frame').html('<div class="custom-alerts alert alert-success" role="alert"><button type="button" class="close" data-dismiss="alert" aria-hidden="true"></button>Cập nhật thông tin thành công</div>');
    }

    function showDangerAlert() {
        $('#alert-frame').html('<div class="custom-alerts alert alert-danger" role="alert"><button type="button" class="close" data-dismiss="alert" aria-hidden="true"></button>Cập nhật thông tin không thành công</div>');
    }

    function loadOverviewTab() {
        $('#contest-from-time').datetimepicker({ format: "DD/MM/YYYY hh:mm A", });
        $('#contest-to-time').datetimepicker({ format: "DD/MM/YYYY hh:mm A" });

        $('#contest-short-desc').summernote({ height: 150 });
        $('#contest-desc').summernote({ height: 150 });
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
        var data = new FormData($('#form-upload-mc-questions').get(0));
        $.ajax({
            url: uploadQuestionsUrl + '?id=' + contestId,
            type: 'POST',
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    showSuccessAlert();
                    loadMCQuestions();
                } else {
                    showDangerAlert();
                }
            },
            error: function(response, error) {
                showDangerAlert();
            }
        });
    }

    function updateMCTestSettings() {
        $.ajax({
            url: updateUrl + '?id=' + contestId,
            type: 'POST',
            data: {
                use_mc_test: $('#use-mctest').prop('checked') == true,
                mc_questions: $('#mctest-questions').val(),
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                if (response.success) {
                    showSuccessAlert();
                } else {
                    showDangerAlert();
                }
            },
            error: function(response, error) {
                showDangerAlert();
            }
        });
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
                contest_time: $('#contest-time').val(),
                maximum_of_matches: $('#contest-maximum-of-matches').val(),
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                if (response.success) {
                    showSuccessAlert();
                } else {
                    showDangerAlert();
                }
            },
            error: function(response, error) {
                showDangerAlert();
            }
        });
    }

    function updateWritingTestSettings() {
        $.ajax({
            url: updateUrl + '?id=' + contestId,
            type: 'POST',
            data: {
                use_writing_test: $('#use-writingtest').prop('checked') == true,
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                if (response.success) {
                    showSuccessAlert();
                } else {
                    showDangerAlert();
                }
            },
            error: function(response, error) {
                showDangerAlert();
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
        var data = new FormData($('#form-upload-writing-questions').get(0));
        $.ajax({
            url: uploadQuestionsUrl + '?id=' + contestId,
            type: 'POST',
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    showSuccessAlert();
                    loadWritingQuestions();
                } else {
                    showDangerAlert();
                }
            },
            error: function(response, error) {
                showDangerAlert();
            }
        });
    }

    function deleteContest() {
        $.ajax({
            url: deleteUrl,
            type: 'GET',
            data: { id: contestId },
            success: function(response) {
                if (response.success) {
                    window.location.href = managementUrl;
                }
            }
        });
    }

    $('#btn-update-overview').on('click', function(e) {
        e.preventDefault();
        updateOverviewInfo();
    });

    $('#btn-update-mc-questions').on('click', function(e) {
        e.preventDefault();
        uploadMCQuestions();
    });

    $('#btn-update-mctest').on('click', function(e) {
        e.preventDefault();
        updateMCTestSettings();
    });

    $('#btn-update-writing-questions').on('click', function(e) {
        e.preventDefault();
        uploadWritingQuestions();
    });

    $('#btn-update-writingtest').on('click', function(e) {
        e.preventDefault();
        updateWritingTestSettings();
    });

    $('#btn-delete').on('click', function(e) {
        e.preventDefault();
        deleteContest();
    });

    loadOverviewTab();
    loadMCQuestions();
    loadWritingQuestions();
});
