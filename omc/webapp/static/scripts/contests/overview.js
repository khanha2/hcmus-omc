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

    function getTime(timer) {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;
        return minutes + ':' + seconds;
    };

    function addMatchToTable(match) {
        var timeString = '';
        if (typeof match.contest_time !== 'undefined') {
            timeString = getTime(match.contest_time);
        } else {
            timeString = '<a class="btn green btn-xs" href="' + contestUrl + '">Đang diễn ra</a>';
        }
        var row = '<tr><td>' + match.match_name + '</td><td>' + timeString + '</td>';
        if (match.use_mc_test) {
            row += '<td>' + match.mc_passed_responses + '</td>';
        }
        row += '</tr>';

        $('#tbody-match-results').append(row);
    };

    function loadMatchList() {
        $.ajax({
            url: matchResultUrl,
            type: 'GET',
            data: { 'id': contestId },
            success: function(response) {
                $(response).each(function(index, element) {
                    addMatchToTable(element);
                });
            },
            error: function(response, error) {}
        });
    };

    loadMatchList();
});
