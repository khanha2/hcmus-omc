$(document).ready(function() {
    function submitExam() {

    }

    function startTimer() {
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

    function loadMCQuestions(questions) {
        for (i = 0; i < questions.length; ++i) {
            $('#tab-mc-questions').find('.general-item-list').append(
                '<div class="item">' +
                '<div class="item-body">' +
                '<strong>Câu hỏi ' + (i + 1) + '</strong>' +
                '<p>' + choice_questions[i].content + '</p>' +
                '<div class="radio-list">' +
                '<label><input type="radio" name="' + choice_questions[i].id + '" value="a"> a. ' + choice_questions[i].a + '</label>' +
                '<label><input type="radio" name="' + choice_questions[i].id + '" value="b"> b. ' + choice_questions[i].b + '</label>' +
                '<label><input type="radio" name="' + choice_questions[i].id + '" value="c"> c. ' + choice_questions[i].c + '</label>' +
                '<label><input type="radio" name="' + choice_questions[i].id + '" value="d"> d. ' + choice_questions[i].d + ' </label>' +
                '</div>' +
                '</div>' +
                '</div>'
            );
        }
    }

    function loadWritingQuestions() {

    }

    function loadData() {

    }

    $('#btn-submit').on('click', function() {
        submitExam();
    });

    loadData();
});
