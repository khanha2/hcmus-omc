$(document).ready(function() {
    function showMessage(message) {
        $('#message').text(message);
        $('#message-form').show();
    }

    function changePassword() {
        $('#message-form').hide();
        if ($('#old-password').val().length === 0) {
            showMessage('Mật khẩu không được rỗng.')
            return;
        }
        if ($('#new-password1').val().length === 0 || $('#new-password2').val().length === 0) {
            showMessage('Mật khẩu mới không được rỗng.');
            return;
        }
        if ($('#new-password1').val() !== $('#new-password2').val()) {
            showMessage('Mật khẩu mới không trùng khớp.');
            return;
        }
        $.ajax({
            url: changePasswordUrl,
            type: 'POST',
            data: {
                old_password: $('#old-password').val(),
                new_password1: $('#new-password1').val(),
                new_password2: $('#new-password2').val(),
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                if (response.success) {
                    windows.location.href = '/';
                } else {
                    showMessage('Không thể đổi mật khẩu.');
                }
            }
        });
    }

    $('.form-control').on('keypress', function(e) {
        if (e.which == 13) {
            changePassword();
        }
    });

    $('#btn-change').on('click', function(e) {
        e.preventDefault();
        changePassword();
    });
});
