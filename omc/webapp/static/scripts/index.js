$(document).ready(function() {
    function loadData() {
        function addItem(element) {
            var timeString = element.time_string == null ? '<em>Chưa có thông tin</em>' : element.time_string;
            var short_description = element.short_description ? element.short_description : 'Chưa có mô tả';
            var row = '<div class="panel panel-default event"><div class="panel-body"><h3><a href="' + contestUrl + '?id=' + element.id + '">' + element.name + '</a></h3><i class="glyphicon glyphicon-time"></i>' + element.time_string + '<p><em>' + element.short_description + '</em></p></div></div>';
            $('#current-contests').append(row);
        }
        $.ajax({
            url: contestsApiUrl,
            type: 'GET',
            data: {},
            success: function(response) {
                $(response).each(function(index, element) {
                    addItem(element);
                });
            }
        });
    }
    loadData();
});
