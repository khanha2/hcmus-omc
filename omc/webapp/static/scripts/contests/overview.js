$(document).ready(function() {
    $('#btn-start').on('click', function(e) {
        e.preventDefault();
        $.ajax({
            url: apiContestUrl,
            type: 'GET',
            data: {
                'id': contestId,
                'generate': ''
            },
            success: function(response) {
                if (response.success) {
                    window.location.href = doContestUrl;
                }
            },
            error: function(response, error) {}
        });
    });

    // var getTime = function(timer) {
    //     minutes = parseInt(timer / 60, 10);
    //     seconds = parseInt(timer % 60, 10);
    //     minutes = minutes < 10 ? "0" + minutes : minutes;
    //     seconds = seconds < 10 ? "0" + seconds : seconds;
    //     return minutes + ':' + seconds;
    // };

    // var addMatchToTable = function(match) {
    //     var timeString = '';
    //     if (typeof match.contest_time !== 'undefined') {
    //         timeString = getTime(match.contest_time);
    //     } else {
    //         timeString = '<a class="btn green btn-xs" href="' + contestUrl + '">Đang diễn ra</a>';
    //     }
    //     $('#matches-table').find('tbody').append(
    //         '<tr>' +
    //         '<td>' + match.fields.match_id + '</td>' +
    //         '<td>' + match.fields.choice_answers_passed + '</td>' +
    //         '<td>' + timeString + '</td>' +
    //         '</tr>'
    //     );
    // };

    // var loadMatchList = function() {
    //     $.ajax({
    //         url: apiAnswersUrl,
    //         type: 'GET',
    //         data: {
    //             'activity_id': activityId,
    //             'user_id': userId
    //         },
    //         success: function(response) {
    //             for (i = 0; i < response.length; ++i) {
    //                 addMatchToTable(response[i]);
    //             }
    //         },
    //         error: function(response, error) {}
    //     });
    // };

    // loadMatchList();
});