$(document).ready(function() {
    var page = 1;

    function addItem(element) {
        var row = '<li class="list-group-item"><div class="pull-right"><a class="btn btn-default btn-sm" href="' + contestUrl + '?id=' + element.id + '"><i class="glyphicon glyphicon-cog"></i></a></div><h4 class="list-group-item-heading">' + element.name + '</h4><p class="list-group-item-text">' + element.from_time + ' - ' + element.to_time + '</p></li>';
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

    loadData();
});
