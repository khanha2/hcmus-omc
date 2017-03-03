$(document).ready(function() {
    var submitExam = function() {
        post_data = {};
        var mcResponses = $('input[type=radio]:checked');
        $(mcResponses).each(function(index, element) {
            post_data['mcr_' + $(element).attr('name')] = $(element).val();
        });
        var writingResponses = $('textarea');
        $(writingResponses).each(function(index, element) {
            post_data['wtr_' + $(element).attr('id')] = $(element).val();
        });
        post_data['csrfmiddlewaretoken'] = csrfToken;
        $.ajax({
            url: apiContestUrl + '?id=' + contestId + '&submit',
            type: 'POST',
            data: post_data,
            success: function(response) {
                console.log(response);
                if (response.success) {
                    window.location.href = contestOverviewUrl;
                }
            },
            error: function(response, error) {}
        });
    };

    var startTimer = function(duration, display) {
        var timer = duration,
            minutes, seconds;
        setInterval(function() {
            minutes = parseInt(timer / 60, 10);
            seconds = parseInt(timer % 60, 10);

            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            if (timer >= 0) {
                display.textContent = minutes + ":" + seconds;
            }
            if (timer <= 0) {
                submitExam();
            }
            --timer;
        }, 1000);
    }
    $('#btn-submit').on('click', function() {
        submitExam();
    });

    startTimer(initRemainingTime, document.querySelector('#time'));
});
