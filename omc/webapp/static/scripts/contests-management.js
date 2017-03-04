$(document).ready(function() {
    var page = 1;

    function initialize() {
        $('#contest-from-time').datetimepicker({ format: "DD/MM/YYYY hh:mm" });
        $('#contest-to-time').datetimepicker({ format: "DD/MM/YYYY hh:mm" });
    }

    function loadData() {
        function addItem(element) {
            var timeString = element.time_string == null ? '<em>Chưa có thông tin</em>' : element.time_string;
            var row = '<li class="list-group-item"><div class="pull-right"><a class="btn btn-default btn-sm" href="' + contestAdminUrl + '?id=' + element.id + '"><i class="glyphicon glyphicon-cog"></i></a></div><h4 class="list-group-item-heading"><a href="' + contestUrl + '?id=' + element.id + '">' + element.name + '</a></h4><p class="list-group-item-text">' + timeString + '</p></li>';
            $('#contests').append(row);
        }
        $.ajax({
            url: contestsApiUrl,
            type: 'GET',
            data: { page: page, management: '' },
            success: function(response) {
                $(response).each(function(index, element) {
                    addItem(element);
                });
            }
        });
    }

    function createContest() {
        $.ajax({
            url: createApiUrl,
            type: 'POST',
            data: {
                name: $('#contest-name').val(),
                from_time: $('#contest-from-time input').val(),
                to_time: $('#contest-to-time input').val(),
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                if (response.success) {
                    window.location.href = contestAdminUrl + '?id=' + response.id;
                }
            }
        });
    }

    $('#btn-create').on('click', function(e) {
        e.preventDefault();
        createContest();
    });

    initialize();
    loadData();
});
