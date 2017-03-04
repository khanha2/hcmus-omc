$(document).ready(function() {
    var totalPages = 0;

    canFind = function() {
        var _canFind = false;
        // if ($('#is-finding').val() == 1) {
        //     var idpfx = $('#find-idpfx').val().trim();
        //     if (idpfx.length > 0) {
        //         _canFind = true;
        //     }
        //     var name = $('#find-name').val().trim();
        //     if (name.length > 0) {
        //         _canFind = true;
        //     }
        // }
        return _canFind;
    }

    function getQueryInfo() {
        var dict = {};
        // if (canFind()) {
        //     var idpfx = $('#find-idpfx').val().trim();
        //     if (idpfx.length > 0) {
        //         dict['idpfx'] = idpfx;
        //     }
        //     var name = $('#find-name').val().trim();
        //     if (name.length > 0) {
        //         dict['name'] = name;
        //     }
        // }
        dict['id'] = contestId;
        return dict;
    }

    function getTime(timeString) {
        minutes = parseInt(timeString / 60, 10);
        seconds = parseInt(timeString % 60, 10);
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;
        return minutes + ':' + seconds;
    }

    function initPages(pages, currentPage = 1) {
        Paginatior('.paginator', pages, loadTable, currentPage, false);
    }

    var loadMatch = function(match) {
        var timeString = '';
        var detail = '';
        if (typeof match.contest_time !== 'undefined') {
            timeString = getTime(match.contest_time);
            detail = '<button class="btn btn-default btn-xs btn-detail" data-id="' + match.pk + '" title="Chi tiết"><i class="glyphicon glyphicon-list"></i></button>';
        }
        var row = '<tr><td>' + match.user_username + '</td><td>' + match.user_fullname + '</td><td>' + match.match_id + '</td><td>' + timeString + '</td>';
        if (match.use_mc_test) {
            row += '<td>' + match.mc_passed_responses + '</td>';
        }
        row += '<td>' + detail + '</td></tr>';
        $('#tbody-contestants').append(row);
    };

    function loadTable(page) {
        page = typeof page !== 'undefined' ? page : 1;
        $currentPage = page;
        var dict = getQueryInfo();
        dict['page'] = page;
        $.ajax({
            type: "GET",
            url: contestantsUrl,
            data: dict,
            dataType: "text",
            success: function(response) {
                var data = JSON.parse(response);
                if (data.pages != totalPages) {
                    totalPages = data.pages;
                    initPages(data.pages, data.page);
                }
                $('#tbody-contestants').empty();
                $(data.data).each(function(index, element) {
                    loadMatch(element);
                });
            },
            error: function(response, error) {
                console.log(response);
            }
        });
    }

    function loadData() {
        loadTable(1);
    }

    loadData();
});
