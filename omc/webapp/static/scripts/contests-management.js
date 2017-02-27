$(document).ready(function() {
    var page = 1;

    function initialize() {
        $('#contest-from-time').datetimepicker();
        $('#contest-to-time').datetimepicker();
    }

    function addItem(element) {
        var timeString = element.time_string == null ? '<em>Chưa có thông tin</em>' : element.time_string;
        var row = '<li class="list-group-item"><div class="pull-right"><a class="btn btn-default btn-sm" href="' + contestUrl + '?id=' + element.id + '"><i class="glyphicon glyphicon-cog"></i></a></div><h4 class="list-group-item-heading">' + element.name + '</h4><p class="list-group-item-text">' + timeString + '</p></li>';
        $('#contests').append(row);
    }

    function loadData() {
        $.ajax({
            url: contestsApiUrl,
            type: 'GET',
            data: { page: page },
            success: function(response) {
                $(response).each(function(index, element) {
                    addItem(element);
                });
            }
        });
    }

    function getFormatedTimeString(timeString) {
        var timeObject = moment(timeString, 'MM/DD/YYYY HH:mm A');
        if (timeObject.isValid()) {
            return timeObject.day() + '/' + timeObject.month() + '/' + timeObject.year() + ' ' + timeObject.hour() + ':' + timeObject.minute();
        }
        return null;
    }

    function createContest() {
        $.ajax({
            url: createApiUrl,
            type: 'POST',
            data: {
                name: $('#contest-name').val(),
                from_time: getFormatedTimeString($('#contest-from-time input').val()),
                to_time: getFormatedTimeString($('#contest-to-time input').val()),
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                if (response.success) {
                    window.location.href = contestUrl + '?id=' + response.id;
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
