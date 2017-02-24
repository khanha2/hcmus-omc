$(document).ready(function() {
    function loadOverviewTab() {
        $('#datetimepicker1').datetimepicker();
        $('#datetimepicker2').datetimepicker();

        $('#contest-short-desc').summernote({ height: 150 });
        $('#contest-desc').summernote({ height: 150 });
    }

    loadOverviewTab();
});
